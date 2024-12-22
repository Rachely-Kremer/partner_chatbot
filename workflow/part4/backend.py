from typing import Annotated, Literal

from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict

from langchain_core.tools import tool

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv


load_dotenv()


@tool
def get_customer_data():
    """Provides customer data"""
    pass


@tool
def get_general_info():
    """Provides answers to general questions"""
    pass


class State(TypedDict):
    messages: Annotated[list, add_messages]
    customer_id: str


graph_builder = StateGraph(State)

tools = [get_customer_data, get_general_info]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_intention_tools = llm.bind_tools(tools)

memory = MemorySaver()

system_intention_template = """
    You are a friendly customer assistant at Partner.
    You are going to greet a customer and assist them with their questions.
"""
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_intention_template),
    MessagesPlaceholder(variable_name="messages_placeholder"),
])
intention_chain = prompt_template | llm_with_intention_tools

#######################

db = SQLDatabase.from_uri("sqlite:///../../docs/demo.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
db_tools = toolkit.get_tools()
llm_with_customer_actions_tools = llm.bind_tools(db_tools)

system_customer_actions_template = """
    You are a friendly customer assistant at Partner.
    You are answering queries about customer_id {customer_id}.
"""
customer_actions_prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_customer_actions_template),
    MessagesPlaceholder(variable_name="messages_placeholder"),
])

customer_actions_chain = customer_actions_prompt_template | llm_with_customer_actions_tools


def intention_detector(state: State):
    result = intention_chain.invoke({"messages_placeholder": state["messages"]})
    return {"messages": result}


def chatbot(state: State):
    return {"messages": [llm_with_intention_tools.invoke(state["messages"])]}


def customer_actions(state: State):
    return {"messages": [customer_actions_chain.invoke({
        "messages_placeholder": state["messages"],
        "customer_id": state["customer_id"]
    })]}


def identify_customer(state: State):
    customer_id = state.get("customer_id")
    if not customer_id:
        customer_id = input("Please insert your customer ID: ")
        secret_code = input("Please insert your secret code: ")
    return {"customer_id": customer_id}


def intent_condition(state: State) -> Literal["customer_data", "general_data", "__end__"]:
    if isinstance(state, list):
        ai_message = state[-1]
    elif isinstance(state, dict) and (messages := state.get("messages", [])):
        ai_message = messages[-1]
    elif messages := getattr(state, "messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "customer_data"
    elif len(ai_message.tool_calls) == 2:
        return "general_data"
    return "__end__"


graph_builder.add_node("intention_detector", intention_detector)
graph_builder.add_node("customer_data", ToolNode([get_customer_data]))
graph_builder.add_node("general_data", ToolNode([get_general_info]))
graph_builder.add_node("identify_customer", identify_customer)
graph_builder.add_node("customer_actions", customer_actions)
graph_builder.add_node("tools", ToolNode(tools=db_tools))
graph_builder.add_edge(START, "intention_detector")
graph_builder.add_conditional_edges(
    "intention_detector",
    intent_condition,
)
graph_builder.add_edge("customer_data", "identify_customer")
graph_builder.add_edge("identify_customer", "customer_actions")
graph_builder.add_edge("tools", "customer_actions")
graph_builder.add_edge("customer_actions", END)
graph_builder.add_edge("general_data", END)


graph = graph_builder.compile(checkpointer=memory)


def stream_graph_updates(user_input: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    events = graph.stream(
        {"messages": [("user", user_input)]}, config, stream_mode="values"
    )
    for event in events:
        event["messages"][-1].pretty_print()


def save_graph_png():
    graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


if __name__ == '__main__':
    save_graph_png()
