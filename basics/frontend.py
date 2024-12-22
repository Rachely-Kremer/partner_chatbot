import gradio as gr

from partner_chatbot.basics.backend import invoke_llm,stream_llm,invoke_with_trim  


if _name_=="_main_":
    with gr.Blocks(fill_height=True) as demo:
       model=gr.Dropdown(["Gemini","OpenAI"],label="Select model:")
       language=gr.Dropdown(["English","Hebrew"],label="Select language:")


       gr.ChatInterface(
           #invoke_llm,
           #stream_llm,
           invoke_with_trim,
           type="messages",
           multimodal=False,
           theme="soft",
           additional_inputes=[
               language,
               model
           ],
       )

    demo.launch(share=False)