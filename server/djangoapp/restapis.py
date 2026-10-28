import requests
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

backend_url = os.getenv('backend_url', default="http://localhost:3030")
if not backend_url or "your backend url" in backend_url:
    backend_url = "http://localhost:3030"

sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")
if not sentiment_analyzer_url or "your code engine" in sentiment_analyzer_url:
    sentiment_analyzer_url = "http://localhost:5050/"


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + str(value) + "&"
    request_url = backend_url + endpoint
    if params:
        request_url = request_url + "?" + params
    print("GET from {} ".format(request_url))
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print("Network exception occurred: {}".format(e))
        return None


import urllib.parse

def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + urllib.parse.quote(text)
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        return response.json()
    except Exception as e:
        print("Network exception occurred: {}".format(e))
        return None
