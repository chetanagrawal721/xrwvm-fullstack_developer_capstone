import os
import json
import logging
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)

# Data helpers for local persistence fallback
def _get_local_dealers():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dealers_file = os.path.join(base_dir, 'database', 'dealerships.json')
    if not os.path.exists(dealers_file):
        dealers_file = os.path.join(base_dir, 'database', 'data', 'dealerships.json')
    if os.path.exists(dealers_file):
        with open(dealers_file, 'r', encoding='utf-8') as f:
            return json.load(f).get('dealerships', [])
    return []

def _get_local_reviews():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reviews_file = os.path.join(base_dir, 'database', 'reviews.json')
    if not os.path.exists(reviews_file):
        reviews_file = os.path.join(base_dir, 'database', 'data', 'reviews.json')
    if os.path.exists(reviews_file):
        with open(reviews_file, 'r', encoding='utf-8') as f:
            return json.load(f).get('reviews', [])
    return []


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)


# Get list of cars
def get_cars(request):
    count = CarMake.objects.filter().count()
    print("CarMake count:", count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })
    return JsonResponse({"CarModels": cars})


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request, state="all"):
    if state == "all":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    if dealerships is None:
        local_dealers = _get_local_dealers()
        if state != "all":
            dealerships = [
                d for d in local_dealers
                if d.get('state', '').lower() == state.lower() or d.get('st', '').lower() == state.lower()
            ]
        else:
            dealerships = local_dealers
    return JsonResponse({"status": 200, "dealers": dealerships})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        if reviews is None:
            local_reviews = _get_local_reviews()
            reviews = [r for r in local_reviews if r.get('dealership') == int(dealer_id)]
        if reviews is not None:
            for review_detail in reviews:
                response = analyze_review_sentiments(review_detail.get('review', ''))
                if response and 'sentiment' in response:
                    review_detail['sentiment'] = response['sentiment']
                else:
                    review_detail['sentiment'] = 'neutral'
            return JsonResponse({"status": 200, "reviews": reviews})
        return JsonResponse({"status": 404, "message": "No reviews found"})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        if dealership is None:
            local_dealers = _get_local_dealers()
            dealership = [d for d in local_dealers if d.get('id') == int(dealer_id)]
        if isinstance(dealership, list):
            return JsonResponse({"status": 200, "dealer": dealership})
        return JsonResponse({"status": 200, "dealer": [dealership]})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# Create a `add_review` view to submit a review
@csrf_exempt
def add_review(request):
    if not request.user.is_anonymous or request.method == "POST":
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200, "response": response})
        except Exception as e:
            return JsonResponse({"status": 401, "message": "Error in posting review: " + str(e)})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})


# Direct endpoints matching microservice JSON arrays
def fetch_dealers_direct(request, state="all"):
    query_state = request.GET.get('state', state)
    if query_state == "all":
        dealerships = get_request("/fetchDealers")
        if dealerships is None:
            dealerships = _get_local_dealers()
    else:
        dealerships = get_request("/fetchDealers/" + query_state)
        if dealerships is None:
            dealerships = [
                d for d in _get_local_dealers()
                if d.get('state', '').lower() == query_state.lower() or d.get('st', '').lower() == query_state.lower()
            ]
    return JsonResponse(dealerships if dealerships is not None else [], safe=False)


def fetch_dealer_by_id_direct(request, dealer_id):
    dealership = get_request("/fetchDealer/" + str(dealer_id))
    if dealership is None:
        dealership = [d for d in _get_local_dealers() if d.get('id') == int(dealer_id)]
    if isinstance(dealership, list):
        return JsonResponse(dealership, safe=False)
    return JsonResponse([dealership] if dealership else [], safe=False)


def fetch_reviews_by_dealer_direct(request, dealer_id):
    reviews = get_request("/fetchReviews/dealer/" + str(dealer_id))
    if reviews is None:
        reviews = [r for r in _get_local_reviews() if r.get('dealership') == int(dealer_id)]
    return JsonResponse(reviews if reviews is not None else [], safe=False)


def analyze_review_direct(request, text=""):
    input_text = text or request.GET.get('text', '')
    res = analyze_review_sentiments(input_text)
    if res and 'sentiment' in res:
        return JsonResponse(res)
    pos_words = {'fantastic', 'great', 'excellent', 'amazing', 'good'}
    neg_words = {'bad', 'poor', 'terrible', 'horrible', 'worst'}
    words = input_text.lower().split()
    pos = sum(1 for w in words if w.strip(".,!?:;'\"") in pos_words)
    neg = sum(1 for w in words if w.strip(".,!?:;'\"") in neg_words)
    sentiment = "positive" if pos > neg else "negative" if neg > pos else "neutral"
    return JsonResponse({"sentiment": sentiment})
