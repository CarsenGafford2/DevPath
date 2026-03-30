from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Load projects data from JSON file
def load_projects():
    data_path = os.path.join(app.root_path, 'data', 'projects.json')
    with open(data_path, 'r') as f:
        projects = json.load(f)
    return projects

# Rule-based filtering function
def filter_projects(projects, skills, level, interest, time):
    filtered = []
    skills_set = set(skill.strip().lower() for skill in skills)
    for project in projects:
        project_skills = set(s.lower() for s in project.get('skills', []))
        # Check if user skills intersect with project skills
        if not skills_set.intersection(project_skills):
            continue
        # Check level match (case insensitive)
        if project.get('level', '').lower() != level.lower():
            continue
        # Check interest match (case insensitive)
        if project.get('interest', '').lower() != interest.lower():
            continue
        # Check time availability: project time should be <= user time
        # Define time levels order for comparison
        time_levels = {'low': 1, 'medium': 2, 'high': 3}
        project_time = time_levels.get(project.get('time', '').lower(), 0)
        user_time = time_levels.get(time.lower(), 0)
        if project_time > user_time:
            continue
        filtered.append(project)
    # Return top 3 matches
    return filtered[:3]

@app.route('/', methods=['GET', 'POST'])
def index():
    projects = load_projects()
    recommendations = []
    if request.method == 'POST':
        # Get form data
        skills_input = request.form.get('skills', '')
        level = request.form.get('level', '')
        interest = request.form.get('interest', '')
        time = request.form.get('time', '')

        # Parse skills input into list
        skills = [s.strip() for s in skills_input.split(',') if s.strip()]

        # Filter projects based on input
        recommendations = filter_projects(projects, skills, level, interest, time)

    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
