from langchain_fireworks import ChatFireworks
from langchain.prompts import PromptTemplate

# Set API key (best to use environment variable)
import os
os.environ["FIREWORKS_API_KEY"] = "fw_3ZkmFLL1sHsm2sH9oqfA1rE5"  # Replace with your actual key

# Initialize LLM
llm = ChatFireworks(
    model="accounts/fireworks/models/deepseek-v3",
    temperature=0,
    max_retries=2,
)





from flask import Flask, request, jsonify, render_template
import requests
import os
import sqlite3
import spacy
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# DB Setup
def create_connection():
    return sqlite3.connect('workout_assistant.db')

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            goal TEXT,
            fitness_level TEXT,
            preferences TEXT,
            workout_history TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_tables()

# Placeholder function
def get_exercises(muscle_group):
    return [
        {"name": f"{muscle_group.title()} Press"},
        {"name": f"{muscle_group.title()} Fly"},
        {"name": f"{muscle_group.title()} Pushup"}
    ]

def get_recommended_exercises(user_preferences, all_exercises):
    if len(all_exercises) > 0:
        return [all_exercises[0]['name'], all_exercises[1]['name']]
    return []


def process_message(user_id, message):
    # Define the prompt format
    template_string = """
    You are a fitness assistant. Respond helpfully and informatively.
    User: {input}
    """
    
    prompt = PromptTemplate(
        template=template_string,
        input_variables=["input"]
    )

    # Format the user message
    _input = prompt.format_prompt(input=message)

    # Call DeepSeek
    response = llm.invoke(_input.to_string())

    # Return the generated content
    return response.content


@app.route('/')
def home():
    return render_template('AIFrontendHTML.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data['message']
    user_id = data.get('user_id', 1)
    response = process_message(user_id, message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
