import os
import json
import nltk
from flask import Flask
from nltk.sentiment import SentimentIntensityAnalyzer

# Configure NLTK data search paths for bundled vader_lexicon
base_dir = os.path.dirname(os.path.abspath(__file__))
nltk.data.path.append(base_dir)
nltk.data.path.append(os.path.join(base_dir, 'sentiment'))
nltk.data.path.append(os.path.abspath(os.path.join(base_dir, '..', '..', '..', 'nltk_data')))

app = Flask("Sentiment Analyzer")

sia = SentimentIntensityAnalyzer()


@app.get('/')
def home():
    return "Welcome to the Sentiment Analyzer. \
    Use /analyze/text to get the sentiment"


@app.get('/analyze/<input_txt>')
def analyze_sentiment(input_txt):

    scores = sia.polarity_scores(input_txt)
    print(scores)
    pos = float(scores['pos'])
    neg = float(scores['neg'])
    neu = float(scores['neu'])
    res = "positive"
    print("pos neg nue ", pos, neg, neu)
    if (neg > pos and neg > neu):
        res = "negative"
    elif (neu > neg and neu > pos):
        res = "neutral"
    res = json.dumps({"sentiment": res})
    print(res)
    return res


if __name__ == "__main__":
    app.run(debug=True, port=5050)
