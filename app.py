from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import random
import subprocess

def get_git_revision_short_hash() -> str:
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
    except subprocess.CalledProcessError as e:
        print("Exception on process, rc=", e.returncode, "output=", e.output)
    return "failure"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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

@app.route('/echo', methods=['POST'])
@cross_origin
def echo():
    return request.json

@app.route('/analyze', methods=['POST'])
@cross_origin()
def send_messages():
    messages = request.json['messages']
    
    result = run_model(messages)
    response = flask.jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

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