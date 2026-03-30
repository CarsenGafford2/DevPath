# Skill to Project Recommender

A beginner-friendly open-source web application that recommends project ideas based on your skills, experience level, area of interest, and available time.

Enter what you know and what you enjoy, and the app returns tailored project ideas complete with feature lists, tech stacks, step-by-step roadmaps, and starter code templates.

---

## Features

- Personalized project recommendations based on skills, level, interest, and time
- Clear roadmap for each recommended project
- Ready-to-run starter code templates for every project
- Simple, clean interface built with plain HTML, CSS, and JavaScript
- Rule-based backend written in Python with Flask
- No database required — all data is stored in a JSON file
- Beginner-friendly codebase with single-line comments throughout

---

## Tech Stack

| Layer    | Technology          |
|----------|---------------------|
| Backend  | Python, Flask       |
| Frontend | HTML, CSS, JavaScript |
| Data     | JSON file           |

---

## Project Structure

```
skill-project-recommender/
|
|-- app.py                  Main Flask application
|-- requirements.txt        Python dependencies
|-- README.md               Project documentation
|-- CONTRIBUTING.md         Contribution guidelines
|-- .gitignore              Git ignore rules
|
|-- data/
|   |-- projects.json       Sample project dataset
|
|-- templates/
|   |-- index.html          Main HTML page
|
|-- static/
|   |-- style.css           Stylesheet
|   |-- script.js           Frontend JavaScript
|
|-- starter_code/
|   |-- expense_tracker.py  Starter template
|   |-- weather_dashboard.html
|   |-- grade_manager.py
|   |-- task_api.py
|   |-- portfolio.html
|   |-- url_shortener.py
|   |-- data_report.py
|
|-- docs/
    |-- project_overview.md Project overview document
```

---

## Setup Instructions

Follow these steps to run the project on your local machine.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/skill-project-recommender.git
cd skill-project-recommender
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- On macOS and Linux:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in your browser

Navigate to `http://127.0.0.1:5000` in any web browser.

---

## How It Works

The recommendation engine in `app.py` uses a simple rule-based scoring system:

1. Each project in `data/projects.json` is scored against the user's inputs.
2. A skill match adds 3 points per matching skill.
3. A level match adds 2 points.
4. An interest match adds 2 points.
5. A time availability match adds 1 point.
6. The top 3 highest-scoring projects are returned.

---

## Adding Your Own Projects

Open `data/projects.json` and add a new object following this format:

```json
{
  "id": 8,
  "title": "Your Project Title",
  "skills": ["Python"],
  "level": "Beginner",
  "interest": "Web",
  "time": "Low",
  "description": "A short description of what this project builds.",
  "features": ["Feature one", "Feature two"],
  "tech_stack": ["Python", "Flask"],
  "roadmap": ["Step 1: ...", "Step 2: ..."],
  "resources": ["Resource name: https://example.com"],
  "starter_code": "starter_code/your_template.py"
}
```

Valid values:
- `level`: `Beginner`, `Intermediate`, `Advanced`
- `interest`: `Web`, `Data`, `Education`, `Automation`, `Games`
- `time`: `Low`, `Medium`, `High`

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to get started.

---

## License

This project is open source and available under the [MIT License](LICENSE).
