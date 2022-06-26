from email.mime import audio
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'secret'

API_KEY = 'ae81dea0-30bd-4397-9ba3-d58726256214'


def search(word):
    r = requests.get(f'https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key=ae81dea0-30bd-4397-9ba3-d58726256214')
    return r.json()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_word():
    word = request.form['word']
    word = word.lower()
    definition = search(word)
    try:
        shortdef = definition[0]['shortdef'][0]
        shortdef = shortdef[0].upper() + shortdef[1:]
        partofspeech = definition[0]['fl']
        word = word[0].upper() + word[1:]
    except:
        return f"<h1>No definition found for '{word}'</h1>"
    return render_template('result.html', definition=shortdef, word=word, partofspeech=partofspeech)

app.run(debug=True, port='8080')