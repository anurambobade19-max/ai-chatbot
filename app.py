from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import sqlite3

app = Flask(__name__)

# Load AI model
chatbot = pipeline("text-generation", model="distilgpt2")

# Initialize Database
def init_db():
    conn = sqlite3.connect('chat_logs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs 
                 (id INTEGER PRIMARY KEY, user_input TEXT, response TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    # Generate response
    response = chatbot(user_input, max_length=50, num_return_sequences=1)[0]['generated_text']
    
    # Save to SQLite
    conn = sqlite3.connect('chat_logs.db')
    c = conn.cursor()
    c.execute('INSERT INTO logs (user_input, response) VALUES (?, ?)', (user_input, response))
    conn.commit()
    conn.close()
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)