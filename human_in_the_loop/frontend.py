from langchain_core.messages import HumanMessage

from partner_chatbot.human_in_the_loop.backend import app

thread={'configureable':{"thread_id":"3"}}
inputs=[HumanMessage(content="search for Partner's customer service contact details")]

for event in app.stream({"messages": inputs},thread,stream_mode="values"):
    event["messages"][-1].pretty_print()

print("\n_____________________________\n")
print("Human-in-the-loop comes here")
print("\n_____________________________\n")

# resume
for event in app.stream(None,thread,stream_node="values"):
    event["messages"][-1].pretty_print()