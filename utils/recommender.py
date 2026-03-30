import json


# Load projects from JSON file
def load_projects():
    try:
        with open('data/projects.json', 'r') as file:
            projects = json.load(file)
            return projects
    except Exception:
        return []


# Check if a project matches user input
def matches_project(user_input, project):
    # Match skill
    if user_input['skill'] not in project.get('skills', []):
        return False

    # Match level
    if user_input['level'] != project.get('level'):
        return False

    # Match interest
    if user_input['interest'] != project.get('interest'):
        return False

    # Match time
    if user_input['time'] != project.get('time'):
        return False

    return True


# Main recommendation function
def recommend_projects(user_input, projects):
    matched_projects = []

    for project in projects:
        if matches_project(user_input, project):
            matched_projects.append(project)

    # Return top 3 results only
    return matched_projects[:3]
