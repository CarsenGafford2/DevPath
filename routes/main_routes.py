from flask import Blueprint, render_template, request, send_file
from utils.recommender import load_projects, recommend_projects

main_routes = Blueprint('main_routes', __name__)


# Home route
@main_routes.route('/', methods=['GET', 'POST'])
def index():
    projects = load_projects()
    recommendations = []
    error = None

    if request.method == 'POST':
        # Get form data
        skill = request.form.get("skill")
        level = request.form.get("level")
        interest = request.form.get("interest")
        time = request.form.get("time")

        # Validate input
        if not skill or not level or not interest or not time:
            error = "Please fill all fields"
        else:
            user_input = {
                "skill": skill,
                "level": level,
                "interest": interest,
                "time": time
            }

            # Get recommendations
            recommendations = recommend_projects(user_input, projects)

    return render_template(
        "index.html",
        recommendations=recommendations,
        error=error
    )


# Project detail route
@main_routes.route('/project/<int:project_id>')
def project_detail(project_id):
    projects = load_projects()

    # Find project by ID
    project = next((p for p in projects if p.get("id") == project_id), None)

    if not project:
        return "Project not found", 404

    return render_template("project.html", project=project)


# Download starter code
@main_routes.route('/download/<path:filename>')
def download_file(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception:
        return "File not found", 404
