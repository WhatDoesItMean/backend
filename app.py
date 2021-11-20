from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import random
import subprocess
import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_git_revision_short_hash() -> str:
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
    except subprocess.CalledProcessError as e:
        print("Exception on process, rc=", e.returncode, "output=", e.output)
    return "failure"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# model_name = 'bigscience/T0_3B'
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
# print('imported model')

API_URL = "https://api-inference.huggingface.co/models/bigscience/T0pp"
headers = {"Authorization": f"Bearer {os.getenv('HUGGING_FACE_TOKEN')}"}

print(API_URL, headers)

def t0pp_query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

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
@cross_origin()
def echo():
    return request.json

@app.route('/analyze', methods=['POST'])
@cross_origin()
def send_messages():
    messages = request.json['messages']
    
    result = run_model(messages)
    return jsonify(result)

def predict_tone(msg):
    prompt_emotion = "Which sentiment among positive, negative, neutral, joking is best represented by the following tweet?"
    # labels = ['anger', 'joy', 'optimism', 'sadness']
    # prompt_irony = "Does this tweet contain irony?"
    # # labels_irony = ['No', 'Yes']
    # prompt_sentiment = "What sentiment does this tweet convey?"
    # # labels_sentiment = ["negative", "neutral", "positive"]
    prompts = [prompt_emotion]

    print(msg)

    output_labels = []
    for prompt in prompts:
        input_text = prompt + ' ' + msg["message"]
        output = t0pp_query({"inputs": input_text })[0]["generated_text"]
        output_labels.append(output)
    
    resulting_tone = map_to_tone(output_labels)

    print("> ", resulting_tone)
    return resulting_tone

def map_to_tone(labels):
    sentiment, = labels
    print(sentiment)
    if sentiment == 'positive':
        return 'pos'
    elif sentiment == 'negative':
        return 'neg'
    return 'neu'
    
def run_model(messages):
    return [
        predict_tone(message)
        for message in messages
    ]

if __name__ == '__main__':
    app.run(debug=True)