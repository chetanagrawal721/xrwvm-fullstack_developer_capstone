# Dealerships Review Application

An end-to-end full stack web application for browsing car dealerships across the United States, viewing dealer details and customer reviews, sentiment analysis on customer feedback, and submitting new reviews with car make and model selections.

## Project Overview
This project was developed as part of the **IBM Full Stack Software Developer Capstone Project**. It demonstrates a modern multi-tier microservices architecture integrating Python/Django, React, Node.js/Express with MongoDB, and an AI-powered Sentiment Analysis microservice.

### Key Features
- **Dealership Directory**: Browse all dealerships nationwide with state filtering (e.g. Kansas, Texas, California, New York, etc.).
- **Dealer Details & Reviews**: Access comprehensive dealership profiles, contact information, and verified customer reviews.
- **Sentiment Analysis**: Microservice built with Python/Flask and NLTK VADER sentiment analysis to evaluate reviews (positive, neutral, negative) with visual sentiment indicators.
- **User Authentication**: Django session-based user registration, login, and logout.
- **Review Submission**: Authenticated users can submit reviews with purchase confirmation, car make, model, and year.
- **Car Inventory Management**: Django admin interface managing Car Make and Car Model relational records.
- **CI/CD Pipeline**: Automated GitHub Actions workflow for code linting with flake8 and test verification.
- **Cloud Deployment**: Containerized with Docker and ready for IBM Cloud Code Engine and Kubernetes.

## Architecture & Technology Stack
- **Frontend**: React.js, HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
- **Backend Application**: Python, Django, Django REST Framework
- **Database Microservice**: Node.js, Express.js, MongoDB / Mongoose
- **Sentiment Analyzer Microservice**: Python, Flask, NLTK
- **Database**: SQLite3 (Django auth & car models), MongoDB (dealerships & reviews)
- **DevOps**: Docker, GitHub Actions CI/CD, IBM Cloud Code Engine

## Setup and Installation

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
python manage.py runserver
```
Navigate to `http://localhost:8000/` in your web browser.