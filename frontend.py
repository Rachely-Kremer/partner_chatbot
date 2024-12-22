import time

from langchain_core.messages import AIMessage

from partner_chatbot import chain
import gradio as gr


def run_chain(message, history):
    full_msg = ""
    for chunk in chain.stream(
           {"language":"Hebrew","text":message},
           stream_mode="messages"):
        full_msg = full_msg + chunk
        # print(full_msg)
        yield full_msg
        # if isinstance(chunk, AIMessage):  # Filter to just model responses
        #     yield chunk.content


if __name__ == "__main__":
    gr.ChatInterface(
        run_chain,
        type="messages",
        multimodal=False,
        title="Translator to Hebrew",
        description="This bot will translate any text to Hebrew.",
        theme="soft",
        # examples=["Hello", "Am I cool?", "Are tomatoes vegetables?"],
        # cache_examples=False,
        # additional_inputs=[
        #     gr.Slider(10, 100),
        # ],
    ).launch(share=False)


