# DevPath: System Architecture

## Overview

DevPath follows a simple and modular architecture based on the Flask framework. The application is designed to be easy to understand, extend, and maintain.

The system is divided into clear layers:
- Routing layer
- Logic layer
- Data layer
- Presentation layer

---

## High-Level Flow

User Input → Flask Routes → Recommendation Logic → Data Filtering → Response → UI Rendering

---

## Component Breakdown

### 1. Routing Layer (`routes/`)

Handles all incoming requests.

- Receives user input from forms
- Calls the recommendation logic
- Sends data to templates for rendering

Main responsibilities:
- URL handling
- Input validation
- Error handling

---

### 2. Logic Layer (`utils/`)

Contains the core recommendation system.

File:
- `recommender.py`

Responsibilities:
- Load project data
- Apply rule-based filtering
- Return relevant project recommendations

---

### 3. Data Layer (`data/`)

Stores project information in a JSON file.

File:
- `projects.json`

Each project contains:
- Title
- Skills
- Level
- Interest
- Time
- Description
- Features
- Tech stack
- Roadmap
- Resources
- Starter code path

---

### 4. Presentation Layer (`templates/` and `static/`)

Responsible for UI rendering.

- `templates/` → HTML pages
- `static/` → CSS and JavaScript

Handles:
- Form display
- Project cards
- Detail pages

---

## Request Flow (Step-by-Step)

1. User fills the form on the homepage  
2. Form data is sent to the backend via POST request  
3. Route processes input and validates it  
4. Recommendation function filters matching projects  
5. Top results are returned  
6. Data is passed to HTML template  
7. Results are displayed as project cards  

---

## Project Detail Flow

1. User clicks "View Details"  
2. Route `/project/<id>` is triggered  
3. Project is fetched from JSON using ID  
4. Detailed page is rendered  

---

## Starter Code Flow

1. Each project has a file path  
2. Download route is triggered  
3. Flask sends file to user  

---

## Design Principles

- Simplicity over complexity  
- Clear separation of concerns  
- Beginner-friendly structure  
- Modular design for easy contributions  

---

## Scalability

The current system can be extended by:

- Replacing rule-based logic with AI/ML models  
- Adding database support (SQLite/PostgreSQL)  
- Introducing user authentication  
- Adding API endpoints  

---

## Summary

DevPath is built using a clean and modular architecture that allows contributors to easily understand, modify, and extend the system without dealing with unnecessary complexity.
