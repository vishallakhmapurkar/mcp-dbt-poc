import gradio as gr
import json

def handle_json_input(json_text):
    try:
        data = json.loads(json_text)
        with open("input.json", "w") as f:
            json.dump(data, f, indent=2)
        return "✅ JSON saved successfully."
    except Exception as e:
        return f"❌ Error: {str(e)}"

gr.Interface(fn=handle_json_input, inputs="textbox", outputs="text", title="Upload JSON for dbt Model").launch()
