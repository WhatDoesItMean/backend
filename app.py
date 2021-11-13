from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"

@app.route('/send', methods=['POST'])
def send_messages():
    messages = request.json['messages']
    
    result = run_model(messages)
    
    return jsonify(result)

def run_model(messages):
    pass