import json

words = {}
with open('static/assets/words.json') as file:
    words = json.load(file)