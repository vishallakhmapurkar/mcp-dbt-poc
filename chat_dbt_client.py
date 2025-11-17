import gradio as gr
import json
from generate_dbt_files_with_llm import generate_dbt_files
from push_to_github import push_to_github
from validate_dbt import validate_dbt

def handle_file_upload(file):
    chat_history = [{"role": "assistant", "content": "👋 JSON file uploaded. Do you want to generate dbt models?"}]
    if file is not None:
        with open(file.name, "r") as f:
            spec = json.load(f)
        return (
            chat_history,
            spec,
            gr.update(visible=True, interactive=True),  # yes_btn
            gr.update(visible=True, interactive=True),  # no_btn
            gr.update(visible=False, value=""),         # status_box
            gr.update(visible=False, interactive=False),# restart_btn
            file                                         # keep file visible
        )
    return chat_history, None, gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), None

def handle_yes(chat_history, spec):
    chat_history.append({"role": "user", "content": "Yes"})
    chat_history.append({"role": "assistant", "content": "🔄 Generating dbt model files..."})
    yield (
        chat_history,
        spec,
        gr.update(visible=True, interactive=False),
        gr.update(visible=True, interactive=False),
        gr.update(visible=True, value="🔄 Generating dbt model files..."),
        gr.update(visible=False),
        file_input,
    )

    # Step 1: Generate dbt files
    result = generate_dbt_files(spec)
    chat_history.append({"role": "assistant", "content": result})
    yield (
        chat_history,
        spec,
        gr.update(visible=True, interactive=False),
        gr.update(visible=True, interactive=False),
        gr.update(visible=True, value="📤 Pushing to GitHub..."),
        gr.update(visible=False),
        file_input,
    )

    # 🚨 Stop if generation failed
    if result.startswith("❌"):
        # End the flow here, re-enable UI
        yield (
            chat_history,
            None,
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True, interactive=True),
            file_input,
        )
        return

    # Step 2: Push to GitHub
    push_result = push_to_github()
    chat_history.append({"role": "assistant", "content": push_result})
    yield (
        chat_history,
        spec,
        gr.update(visible=True, interactive=False),
        gr.update(visible=True, interactive=False),
        gr.update(visible=True, value="🧪 Running dbt debug, run, docs generate, and test..."),
        gr.update(visible=False),
        file_input,
    )

    # Step 3: Validate dbt
    validate_result = validate_dbt()
    chat_history.append({"role": "assistant", "content": validate_result})
    yield (
        chat_history,
        None,
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=True, interactive=True),
        file_input,
    )

def handle_no(chat_history):
    chat_history.append({"role": "user", "content": "No"})
    chat_history.append({"role": "assistant", "content": "Okay, dbt model generation canceled."})
    return chat_history, None, gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True, interactive=True), None

def handle_restart():
    chat_history = [{"role": "assistant", "content": "👋 Welcome to the dbt Model Generator! Upload a JSON file to get started."}]
    return chat_history, None, gr.update(visible=False), gr.update(visible=False), gr.update(visible=False, value=""), gr.update(visible=False, interactive=False), None

with gr.Blocks() as demo:
    gr.Markdown("### 💬 dbt Model Generator Chat")

    chatbox = gr.Chatbot(label="Chat", type="messages")
    file_input = gr.File(label="Upload JSON File", interactive=True)
    status_box = gr.Textbox(label="Processing Status", interactive=False, visible=False)

    yes_btn = gr.Button("Yes", variant="primary", visible=False)
    no_btn = gr.Button("No", variant="secondary", visible=False)
    restart_btn = gr.Button("🔁 Restart Chat", variant="secondary", visible=False)

    chat_state = gr.State([])
    spec_state = gr.State(None)

    file_input.upload(
        fn=handle_file_upload,
        inputs=[file_input],
        outputs=[chatbox, spec_state, yes_btn, no_btn, status_box, restart_btn, file_input]
    )

    yes_btn.click(
        fn=handle_yes,
        inputs=[chatbox, spec_state],
        outputs=[chatbox, spec_state, yes_btn, no_btn, status_box, restart_btn, file_input],
        concurrency_limit=1,
        show_progress=True
    )

    no_btn.click(
        fn=handle_no,
        inputs=[chatbox],
        outputs=[chatbox, spec_state, yes_btn, no_btn, status_box, restart_btn, file_input]
    )

    restart_btn.click(
        fn=handle_restart,
        outputs=[chatbox, spec_state, yes_btn, no_btn, status_box, restart_btn, file_input]
    )

demo.launch()
