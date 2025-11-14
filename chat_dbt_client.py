import gradio as gr
import json
from generate_dbt_files import generate_dbt_files
from push_to_github import push_to_github
from validate_dbt import validate_dbt

chat_history = []
spec_data = None

def handle_file_upload(file):
    global spec_data, chat_history
    with open(file.name, "r") as f:
        spec_data = json.load(f)
    chat_history.clear()
    chat_history.append({"role": "user", "content": "Uploaded JSON file."})
    chat_history.append({"role": "assistant", "content": "Do you want to generate dbt models?"})
    return chat_history, gr.update(visible=True)

def handle_yes():
    global spec_data, chat_history
    if spec_data:
        chat_history.append({"role": "user", "content": "Yes"})
        result = generate_dbt_files(spec_data)
        push_result = push_to_github()
        validate_result = validate_dbt()
        chat_history.append({"role": "assistant", "content": result + "\n" + push_result + "\n" + validate_result})
        spec_data = None
    else:
        chat_history.append({"role": "user", "content": "Yes"})
        chat_history.append({"role": "assistant", "content": "Please upload a JSON file first."})
    return chat_history, gr.update(visible=False)

def handle_no():
    global chat_history
    chat_history.append({"role": "user", "content": "No"})
    chat_history.append({"role": "assistant", "content": "Okay, dbt model generation canceled."})
    return chat_history, gr.update(visible=False)

with gr.Blocks() as demo:
    gr.Markdown("### 💬 dbt Model Generator Chat")

    file_input = gr.File(label="Upload JSON File")
    chatbox = gr.Chatbot(label="Chat", type="messages")
    with gr.Row(visible=False) as button_row:
        yes_btn = gr.Button("Yes", variant="primary")
        no_btn = gr.Button("No", variant="secondary")

    file_input.change(fn=handle_file_upload, inputs=file_input, outputs=[chatbox, button_row])
    yes_btn.click(fn=handle_yes, outputs=[chatbox, button_row])
    no_btn.click(fn=handle_no, outputs=[chatbox, button_row])

demo.launch()
