from flask import Flask, jsonify, request
from ai import user_input, convert_pdfs_to_vectors
from gemini import chat_with_gemini

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Welcome to the SalesAutomation App Backend.")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    response = user_input(message)
    return jsonify(response)

@app.route('/vectorize', methods=['GET'])
def vectorize():
    print("Vectorizing data...")
    convert_pdfs_to_vectors()
    print("Data vectorized successfully.")
    return jsonify(message="Data vectorized successfully")

@app.route('/summary', methods=['POST'])
def summary():
    text = request.get_json().get('text')
    response = chat_with_gemini(text, history=[])
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
