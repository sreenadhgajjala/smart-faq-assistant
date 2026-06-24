import json
import re

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    return text.strip()

def load_faqs():
    with open("faqs.json", "r", encoding="utf-8") as f:
        return json.load(f)

    tokens = [
        word
        for word in tokens
        if word not in stop_words
        and word not in string.punctuation
    ]

    return " ".join(tokens)

def load_faqs():

    with open(
        "faqs.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)