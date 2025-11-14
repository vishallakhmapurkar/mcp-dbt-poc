import ollama

def generate_sql_model(prompt: str) -> str:
    response = ollama.chat(
        model='gemma',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']
