# fullstack_developer_capstone

**Repository Name**: xrwvm-fullstack_developer_capstone  
**Project Name**: fullstack_developer_capstone  
**Public Repository**: https://github.com/chetanagrawal721/xrwvm-fullstack_developer_capstone  

## Project Overview
An end-to-end full stack web application developed as part of the **IBM Full Stack Software Developer Capstone Project** (`fullstack_developer_capstone`). The application allows users to browse car dealerships across the United States, view dealer details and customer reviews, analyze review sentiment using natural language processing (positive, neutral, negative), and submit new dealership reviews.

### Repository Details
- **Repository Name**: xrwvm-fullstack_developer_capstone
- **Project Name**: fullstack_developer_capstone
- **Author**: Chetan Agrawal
- **GitHub**: https://github.com/chetanagrawal721

### Architecture & Technology Stack
- **Frontend**: React.js, HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
- **Backend Application**: Python, Django, Django REST Framework
- **Database Microservice**: Node.js, Express.js, MongoDB / Mongoose
- **Sentiment Analyzer Microservice**: Python, Flask, NLTK (VADER Lexicon)
- **Database**: SQLite3 (Django auth & car models), MongoDB (dealerships & reviews)
- **DevOps / CI/CD**: Docker, Docker Compose, Kubernetes, GitHub Actions CI/CD, Cloud Deployment

---

## Architecture Diagram & Microservices

```
       +---------------------------------------------+
       |           Client Web Browser                |
       +---------------------------------------------+
                              |
                              v
       +---------------------------------------------+
       |         Django Application (Port 8000)      |
       |  - React Frontend (Single Page Application) |
       |  - User Auth / Session Management           |
       |  - CarMake & CarModel Relational API        |
       |  - Django Admin Dashboard                   |
       +---------------------------------------------+
                 /                         \
                / (HTTP GET/POST)           \ (HTTP GET)
               v                             v
+-------------------------------+  +-------------------------------+
| Database Service (Port 3030)  |  | Sentiment Service (Port 5050) |
| - Express.js & Mongoose       |  | - Flask API                   |
| - Dealerships & Reviews       |  | - NLTK SentimentIntensity     |
| - MongoDB Container (27017)   |  |   Analyzer (VADER Lexicon)    |
+-------------------------------+  +-------------------------------+
```

---

## Setup and Running

### 1. Sentiment Analysis Microservice (Port 5050)
```bash
cd server/djangoapp/microservices
pip install -r requirements.txt
python app.py
```

### 2. Database Microservice (Port 3030)
```bash
cd server/database
npm install
npm start
```

### 3. Django Application & React Frontend (Port 8000)
```bash
# Build React frontend
cd server/frontend
npm install
npm run build

# Start Django backend
cd ..
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 8000
```

### 4. Running with Docker Compose
```bash
docker-compose up --build
```

---

## 28-Task Grading Rubric Evidence Summary

| Task | Description | Evidence / File Path | Status |
|:---:|:---|:---|:---:|
| 1 | Public GitHub URL of README.md with Project name | `README.md` | Verified |
| 2 | Terminal output showing Django server running | `django_server` | Captured |
| 3 | Public GitHub URL of About.html | `server/frontend/static/About.html` | Verified |
| 4 | Public GitHub URL of Contact.html | `server/frontend/static/Contact.html` | Verified |
| 5 | cURL command & output for user login | `loginuser` | Captured |
| 6 | cURL command & output for user logout | `logoutuser` | Captured |
| 7 | Public GitHub URL of Register.jsx with 5 fields | `server/frontend/src/components/Register/Register.jsx` | Verified |
| 8 | cURL command & output for dealer reviews | `getdealerreviews` | Captured |
| 9 | cURL command & output for all dealers | `getalldealers` | Captured |
| 10 | cURL command & output for dealer by ID | `getdealerbyid` | Captured |
| 11 | cURL command & output for dealers in Kansas | `getdealersbyState` | Captured |
| 12 | Screenshot of root user login on admin page | `admin_login.png` | Captured |
| 13 | Screenshot of root user logout from admin page | `admin_logout.png` | Captured |
| 14-15 | cURL command & output for car makes and models | `getallcarmakes` | Captured |
| 16 | cURL command & output for sentiment analysis | `analyzereview` | Captured |
| 17 | Screenshot of dealers on home page before login | `get_dealers.png` | Captured |
| 18 | Screenshot of dealers on home page after login | `get_dealers_loggedin.png` | Captured |
| 19 | Screenshot of dealers filtered by State (Kansas) | `dealersbystate.png` | Captured |
| 20 | Screenshot of dealer details & reviews with endpoint | `dealer_id_reviews.png` | Captured |
| 21 | Screenshot of Post Review page before submission | `dealership_review_submission.png` | Captured |
| 22 | Screenshot of posted review | `added_review.png` | Captured |
| 23 | Terminal output showing GitHub Actions workflow running | `CICD` | Verified |
| 24 | Deployment URL of Django application | `deploymentURL` | Captured |
| 25 | Screenshot of deployed landing page | `deployed_landingpage.png` | Captured |
| 26 | Screenshot of deployed logged-in page | `deployed_loggedin.png` | Captured |
| 27 | Screenshot of deployed dealer details page | `deployed_dealer_detail.png` | Captured |
| 28 | Screenshot of deployed review page | `deployed_add_review.png` | Captured |
