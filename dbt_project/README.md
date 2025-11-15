💬 dbt Model Generator Chat
An interactive chat app that generates dbt models from a JSON specification.


🚀 Features
Upload a JSON spec to define your data models

Chat interface guides you through model generation

Automatically generates dbt files

Pushes models to GitHub

Runs dbt debug, run, docs generate, and test

Displays results and offers restart option

🛠 Setup
Install dependencies:

Code
pip install -r requirements.txt
▶️ Launch the App
Code
python chat_dbt_client.py
📁 Project Structure
Code
dbt_model_generator/
├── chat_dbt_client.py         # Main Gradio app
├── generate_dbt_files.py      # Generates dbt models from JSON
├── push_to_github.py          # Commits and pushes to GitHub
├── validate_dbt.py            # Runs dbt commands
├── requirements.txt           # Python dependencies
└── README.md                  # You're reading it!
🧪 Example Workflow
Upload your JSON file

App asks: “Do you want to generate dbt models?”

Click “Yes” to begin

Models are generated and pushed to GitHub

dbt commands run: debug, run, docs generate, test

Results shown in chat

Click “Restart” to begin again