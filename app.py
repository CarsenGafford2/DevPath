from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load project data
def load_projects():
    with open('data/projects.json', 'r') as file:
        return json.load(file)

# Recommendation logic (rule-based)
def recommend_projects(user_input, projects):
    results = []

    for project in projects:
        # Match skill
        if user_input['skill'] not in project['skills']:
            continue

        # Match level
        if user_input['level'] != project['level']:
            continue

        # Match interest
        if user_input['interest'] != project['interest']:
            continue

        # Match time
        if user_input['time'] != project['time']:
            continue

        results.append(project)

    return results[:3]  # Return top 3

@app.route('/', methods=['GET', 'POST'])
def index():
    projects = load_projects()
    recommendations = []

    if request.method == 'POST':
        user_input = {
            "skill": request.form.get("skill"),
            "level": request.form.get("level"),
            "interest": request.form.get("interest"),
            "time": request.form.get("time")
        }

        recommendations = recommend_projects(user_input, projects)

    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
