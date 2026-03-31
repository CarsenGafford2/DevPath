# DevPath — Skill to Project Recommender

A beginner-friendly, open-source web application that recommends real coding
projects based on your skills, experience level, area of interest, and time
availability. Every recommendation comes with a full step-by-step roadmap,
curated learning resources, and a ready-to-run starter code template.

---

## Problem Statement

Most developers — especially beginners — know they should build projects to
grow their skills, but they spend hours asking "what should I build?" DevPath
solves this by turning four simple inputs into actionable project ideas that
match exactly where you are right now.

---

## Features

- Skill-based project matching using a rule-based scoring algorithm
- Quick-select chip interface for picking skills
- Per-field form validation with clear error messages
- Project detail pages with feature lists, roadmaps, and resources
- Inline starter code viewer with syntax highlighting
- One-click starter code download
- Fully responsive layout for mobile and desktop
- Custom 404 and 500 error pages
- Clean modular codebase suited for open-source contributions

---

## Screenshots

> Screenshots will be added once the project is deployed. To see the UI
> locally, follow the setup steps below and visit http://127.0.0.1:5000.

---

## Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Backend    | Python 3.8+, Flask 3    |
| Frontend   | HTML5, CSS3, JavaScript |
| Data store | JSON file               |
| Tests      | Built-in unittest / pytest |

---

## Project Structure

```
devpath/
|
|-- app.py                      Application entry point
|-- requirements.txt            Python dependencies
|
|-- routes/
|   |-- __init__.py
|   |-- main_routes.py          All Flask routes as a Blueprint
|
|-- utils/
|   |-- __init__.py
|   |-- data_loader.py          JSON reading and project lookup
|   |-- recommender.py          Scoring and filtering logic
|   |-- file_server.py          Starter code resolution and serving
|
|-- data/
|   |-- projects.json           Project dataset
|
|-- templates/
|   |-- index.html              Homepage
|   |-- project.html            Project detail page
|   |-- 404.html                Not found page
|   |-- 500.html                Server error page
|
|-- static/
|   |-- style.css               Stylesheet
|   |-- script.js               Client-side JavaScript
|
|-- starter_code/               Ready-to-run starter templates
|   |-- expense_tracker.py
|   |-- weather_dashboard.html
|   |-- grade_manager.py
|   |-- task_api.py
|   |-- portfolio.html
|   |-- url_shortener.py
|   |-- data_report.py
|
|-- tests/
|   |-- __init__.py
|   |-- test_basic.py           Test suite (27 tests)
|
|-- docs/
|   |-- project_overview.md     High-level project description
|   |-- architecture.md         System design and data flow
|   |-- contribution_guide.md   Onboarding guide for new contributors
|
|-- README.md
|-- CONTRIBUTING.md
|-- CODE_OF_CONDUCT.md
|-- LICENSE
```

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip
- Git

### 1. Clone the repository

```bash
git clone https://github.com/your-username/devpath.git
cd devpath
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
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

Open http://127.0.0.1:5000 in your browser.

### 5. Run the tests

```bash
python tests/test_basic.py
```

Or with pytest:

```bash
pip install pytest
pytest tests/
```

---

## How It Works

1. The user enters their skills, selects a level, interest area, and time availability.
2. The frontend sends a POST request to `/api/recommend`.
3. `utils/recommender.py` scores every project in `data/projects.json` against the inputs.
4. Each matching criterion (skill, level, interest, time) adds points to the score.
5. The top three scoring projects are returned and rendered as cards.
6. Clicking "View Full Project" opens the detail page at `/project/<id>`.
7. The detail page shows features, a visual roadmap timeline, resources, and starter code options.

For a complete breakdown of the scoring algorithm, see `docs/architecture.md`.

---

## Adding Your Own Projects

Open `data/projects.json` and add a new object following this schema:

```json
{
  "id": 8,
  "title": "Your Project Title",
  "skills": ["Python", "Flask"],
  "level": "Beginner",
  "interest": "Web",
  "time": "Medium",
  "description": "One paragraph description.",
  "features": ["Feature one", "Feature two"],
  "tech_stack": ["Python", "Flask", "JSON"],
  "roadmap": ["Step 1: ...", "Step 2: ..."],
  "resources": ["Resource name: https://example.com"],
  "starter_code": "starter_code/your_file.py"
}
```

Valid field values:

| Field      | Accepted values                                   |
|------------|---------------------------------------------------|
| `level`    | `Beginner`, `Intermediate`, `Advanced`            |
| `interest` | `Web`, `Data`, `Education`, `Automation`, `Games` |
| `time`     | `Low`, `Medium`, `High`                           |

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) for
setup instructions, code style guidelines, and the PR process.

First-time contributors should look for issues labeled
**good first issue** on the GitHub Issues page.

---

## Future Scope

- User accounts and saved project bookmarks
- Dark mode toggle
- Search and filter on the results page
- Community-submitted project contributions
- Integration with GitHub to auto-create repos from starter code
- Project difficulty ratings from users

---

## License

This project is open source and available under the [MIT License](LICENSE).
