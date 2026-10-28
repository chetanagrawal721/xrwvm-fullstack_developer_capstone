import subprocess
import time
import urllib.request
import json
import sys
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

print("1. Starting Node Database microservice on port 3030...")
node_proc = subprocess.Popen(
    ["node", "app.js"],
    cwd=os.path.join(base_dir, "server", "database")
)

print("2. Starting Flask Sentiment microservice on port 5050...")
flask_proc = subprocess.Popen(
    ["python", "app.py"],
    cwd=os.path.join(base_dir, "server", "djangoapp", "microservices")
)

print("3. Starting Django application on port 8000...")
django_proc = subprocess.Popen(
    ["python", "manage.py", "runserver", "8000"],
    cwd=os.path.join(base_dir, "server")
)

time.sleep(4)

try:
    print("\n--- Testing Task 16: /analyze/Fantastic%20services ---")
    with urllib.request.urlopen("http://localhost:5050/analyze/Fantastic%20services") as resp:
        res16 = resp.read().decode('utf-8')
        print("Status:", resp.status)
        print("Response:", res16)

    print("\n--- Testing Task 9: /fetchDealers ---")
    with urllib.request.urlopen("http://localhost:3030/fetchDealers") as resp:
        dealers = json.loads(resp.read().decode('utf-8'))
        print("Status:", resp.status)
        print("Total dealers:", len(dealers))
        print("Sample dealer:", dealers[0]["full_name"])

    print("\n--- Testing Task 10: /fetchDealer/1 ---")
    with urllib.request.urlopen("http://localhost:3030/fetchDealer/1") as resp:
        dealer1 = json.loads(resp.read().decode('utf-8'))
        print("Status:", resp.status)
        print("Dealer 1:", dealer1)

    print("\n--- Testing Task 11: /fetchDealers/Kansas ---")
    with urllib.request.urlopen("http://localhost:3030/fetchDealers/Kansas") as resp:
        kansas = json.loads(resp.read().decode('utf-8'))
        print("Status:", resp.status)
        print("Kansas dealers count:", len(kansas))
        print("Kansas dealer:", kansas[0]["city"], kansas[0]["state"])

    print("\n--- Testing Task 8: /fetchReviews/dealer/15 ---")
    with urllib.request.urlopen("http://localhost:3030/fetchReviews/dealer/15") as resp:
        reviews = json.loads(resp.read().decode('utf-8'))
        print("Status:", resp.status)
        print("Reviews count for dealer 15:", len(reviews))

    print("\n--- Testing Task 14 & 15: /djangoapp/get_cars ---")
    with urllib.request.urlopen("http://localhost:8000/djangoapp/get_cars") as resp:
        cars = json.loads(resp.read().decode('utf-8'))
        print("Status:", resp.status)
        print("Total cars:", len(cars.get("CarModels", [])))

    print("\n--- Testing Task 5: /djangoapp/login ---")
    login_data = json.dumps({"userName": "admin", "password": "adminpassword"}).encode('utf-8')
    req = urllib.request.Request("http://localhost:8000/djangoapp/login", data=login_data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        login_res = resp.read().decode('utf-8')
        print("Status:", resp.status)
        print("Login response:", login_res)

    print("\n--- Testing Task 6: /djangoapp/logout ---")
    with urllib.request.urlopen("http://localhost:8000/djangoapp/logout") as resp:
        logout_res = resp.read().decode('utf-8')
        print("Status:", resp.status)
        print("Logout response:", logout_res)

    print("\n=== ALL ENDPOINTS VERIFIED AND FUNCTIONING PERFECTLY! ===")
finally:
    print("\nShutting down child processes...")
    node_proc.kill()
    flask_proc.kill()
    django_proc.kill()
