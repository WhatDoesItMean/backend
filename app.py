from flask import Flask, request, jsonify
import random
import subprocess

def get_git_revision_short_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

app = Flask(__name__)

API_VERSION_NUMBER = "0.1"
TONES = [
    "j", # "joking"
    "hj", # "half-joking"
    "s", # "sarcastic"
    "gen", # "genuine"
    "srs", # "serious"
    "nsrs", # "non-serious"
    "pos", # "positive"
    "neu", # "neutral"
    "neg", # "negative"
    "p", # "platonic"
    "r", # "romantic"
    "c", # "copypasta"
    "l", # "lyrics"
    "lh", # "light-hearted"
    "nm", # "not mad"
    "lu", # "a little upset"
    "nbh", # "directed at nobody here"
    "nsb", # "not subtweeting"
    "sx", # "sexual intent"
    "nsx", # "non-sexual intent"
    "rh", # "rhetorical question"
    "t", # "teasing"
    "ij", # "inside joke"
    "m", # "metaphorically"
    "li", # "literally"
    "hyp", # "hyperbole"
    "f", # "fake"
    "th", # "threat"
    "cb", # "clickbait"
]

@app.route('/')
def index():
    return {
        "app": "tonify",
        "version": API_VERSION_NUMBER,
        "hash": get_git_revision_short_hash()
    }

@app.route('/analyze', methods=['POST'])
def send_messages():
    messages = request.json['messages']
    
    result = run_model(messages)
    
    return jsonify(result)

def create_random_prediction():
    return {
        tone: random.random()
        for tone in TONES
    }

def run_model(messages):
    return [
        create_random_prediction()
        for message in messages
    ]

if __name__ == '__main__':
    app.run(debug=True)