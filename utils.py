import json
import nltk
import string

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download("punkt")
nltk.download("stopwords")

def preprocess(text):

    text = text.lower()

    tokens = word_tokenize(text)

    stop_words = set(
        stopwords.words("english")
    )

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