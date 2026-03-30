import json

# Load project data from JSON
def load_projects():
    try:
        with open('data/projects.json', 'r') as file:
            return json.load(file)
    except Exception:
        return []

# Rule-based recommendation system
def recommend_projects(user_input, projects):
    results = []

    for project in projects:
        # Match skill
        if user_input['skill'] not in project.get('skills', []):
            continue

        # Match level
        if user_input['level'] != project.get('level'):
            continue

        # Match interest
        if user_input['interest'] != project.get('interest'):
            continue

        # Match time
        if user_input['time'] != project.get('time'):
            continue

        results.append(project)

    # Return top 3 projects
    return results[:3]
