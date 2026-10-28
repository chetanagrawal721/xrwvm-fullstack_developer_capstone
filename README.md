# fullstack_developer_capstone

**Repository Name**: xrwvm-fullstack_developer_capstone  
**Project Name**: fullstack_developer_capstone  

## Project Overview
An end-to-end full stack web application developed as part of the **IBM Full Stack Software Developer Capstone Project** (`fullstack_developer_capstone`). The application allows users to browse car dealerships across the United States, view dealer details and customer reviews, analyze review sentiment using natural language processing (positive, neutral, negative), and submit new dealership reviews.

### Repository Details
- **Repository Name**: xrwvm-fullstack_developer_capstone
- **Project Name**: fullstack_developer_capstone
- **Author**: Harshal Khade

### Architecture & Technology Stack
- **Frontend**: React.js, HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
- **Backend Application**: Python, Django, Django REST Framework
- **Database Microservice**: Node.js, Express.js, MongoDB / Mongoose
- **Sentiment Analyzer Microservice**: Python, Flask, NLTK
- **Database**: SQLite3 (Django auth & car models), MongoDB (dealerships & reviews)
- **DevOps**: Docker, GitHub Actions CI/CD, Cloud Deployment

## Setup and Running

### 1. Sentiment Analysis Microservice
```bash
cd server/djangoapp/microservices
pip install -r requirements.txt
python app.py
```

### 2. Database Microservice
```bash
cd server/database
npm install
npm start
```

### 3. Django Application & React Frontend
```bash
cd server
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python3 manage.py runserver
```