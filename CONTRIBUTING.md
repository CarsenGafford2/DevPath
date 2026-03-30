# Contributing to Skill to Project Recommender

Thank you for your interest in contributing. This project is built for learners, so all skill levels are welcome. Below are simple steps to make your first contribution.

---

## Before You Start

- Read the README.md to understand how the project works
- Look at the open issues on GitHub for tasks labeled `good first issue`
- Make sure you have Python 3.8 or higher and Git installed

---

## Step 1: Fork the Repository

Click the Fork button on the top-right of the GitHub repository page. This creates a personal copy of the project under your GitHub account.

---

## Step 2: Clone Your Fork

```bash
git clone https://github.com/your-username/skill-project-recommender.git
cd skill-project-recommender
```

---

## Step 3: Create a New Branch

Always create a new branch for your changes. Never work directly on the `main` branch.

```bash
git checkout -b your-branch-name
```

Use a short, descriptive branch name, for example:

- `fix-form-validation`
- `add-new-projects`
- `improve-card-layout`

---

## Step 4: Make Your Changes

- Follow the existing code style and structure
- Add a short single-line comment above any new logic you write
- If adding new projects to `projects.json`, follow the existing data format
- If adding a new starter code file, place it in the `starter_code/` folder

---

## Step 5: Test Your Changes Locally

Start the Flask server and verify your changes work as expected:

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` and test the feature you changed.

---

## Step 6: Commit Your Changes

Write a clear and short commit message that describes what you changed:

```bash
git add .
git commit -m "Add three new beginner Python projects to dataset"
```

Avoid vague messages like "fix stuff" or "update".

---

## Step 7: Push and Open a Pull Request

```bash
git push origin your-branch-name
```

Then go to your fork on GitHub and click "Compare and pull request". Fill in:

- A short title describing your change
- A brief description of what you changed and why

---

## Code Guidelines

- Keep code simple and easy to read for beginners
- Do not use advanced libraries or frameworks not already in the project
- Follow the existing naming style: lowercase with underscores for Python, camelCase for JavaScript
- Do not leave unused code or debug print statements in your submission
- One feature or fix per pull request — keep changes focused

---

## Questions

If you are unsure about anything, open a GitHub Discussion or comment on the relevant issue. No question is too basic.
