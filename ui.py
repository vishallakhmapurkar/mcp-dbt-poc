import gradio as gr
import requests
import json

def generate_and_save_all(json_file):
    spec = json.load(open(json_file.name))
    response = requests.post("http://localhost:8000/generate_and_save_all", json=spec).json()

    outputs = []
    for model in response["models"]:
        if model["status"] == "auto":
            badge = "⚡ Auto-generated (staging)"
        elif model["status"] == "valid":
            badge = "✅ Valid SQL"
        else:
            badge = "❌ Fallback used"
        outputs.append(f"### {model['table']} ({model['model_type']})\n{badge}\nSaved as {model['filename']}")

    return "\n\n".join(outputs) + f"\n\n{response['git_status']}", response["schema_preview"]

with gr.Blocks() as demo:
    gr.Markdown("## dbt + BigQuery SQL Generator (Staging + Mart + Sources + Git Push)")

    json_file = gr.File(label="Upload JSON Spec", file_types=[".json"])
    output_sql = gr.Textbox(label="Generation & Save Status", lines=30)
    schema_preview = gr.Textbox(label="Updated schema.yml Preview", lines=15)

    btn_generate = gr.Button("Generate + Save All Models (with Sources + Git Push)")
    btn_generate.click(generate_and_save_all, [json_file], [output_sql, schema_preview])

demo.launch()
