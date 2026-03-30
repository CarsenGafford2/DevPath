# app.py - Main Flask application for DevPath (Skill to Project Recommender)

from flask import Flask, render_template, request, jsonify, send_from_directory, abort
import json
import os

app = Flask(__name__)

# Absolute path to the data file so it works from any working directory
DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "projects.json")

# Absolute path to the starter code folder
STARTER_CODE_DIR = os.path.join(os.path.dirname(__file__), "starter_code")


# ============================================================
# Data helpers
# ============================================================

def load_projects():
    # Read and return all projects from the JSON file
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def get_project_by_id(project_id):
    # Return a single project matching the given integer ID, or None if not found
    projects = load_projects()
    for project in projects:
        if project.get("id") == project_id:
            return project
    return None


# ============================================================
# Recommendation logic
# ============================================================

def score_project(project, user_skills, level, interest, time_availability):
    # Compute a relevance score for one project against the user's inputs
    score = 0

    # Skill match: 3 points per matched skill (weighted highest)
    project_skills = [s.lower() for s in project.get("skills", [])]
    skill_matches = sum(1 for s in user_skills if s in project_skills)
    score += skill_matches * 3

    # Level match: 2 points
    if project.get("level", "").lower() == level.lower():
        score += 2

    # Interest match: 2 points
    if project.get("interest", "").lower() == interest.lower():
        score += 2

    # Time availability match: 1 point
    if project.get("time", "").lower() == time_availability.lower():
        score += 1

    return score


def filter_projects(skills, level, interest, time_availability):
    # Parse the comma-separated skills string into a lowercase list
    user_skills = [s.strip().lower() for s in skills.split(",") if s.strip()]

    all_projects = load_projects()
    scored = []

    for project in all_projects:
        score = score_project(project, user_skills, level, interest, time_availability)
        # Only include projects that matched on at least one criterion
        if score > 0:
            scored.append({"project": project, "score": score})

    # Sort by descending score so the best matches appear first
    scored.sort(key=lambda x: x["score"], reverse=True)

    # Return up to the top 3 matching projects
    return [item["project"] for item in scored[:3]]


# ============================================================
# Routes
# ============================================================

@app.route("/")
def index():
    # Render the main search/recommendation page
    return render_template("index.html")


@app.route("/api/recommend", methods=["POST"])
def recommend():
    # Accept a JSON body and return matching project recommendations
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    # Extract and strip all input fields
    skills = data.get("skills", "").strip()
    level = data.get("level", "").strip()
    interest = data.get("interest", "").strip()
    time_availability = data.get("time", "").strip()

    # Validate that all required fields are present
    if not skills:
        return jsonify({"error": "Please enter at least one skill."}), 400
    if not level:
        return jsonify({"error": "Please select an experience level."}), 400
    if not interest:
        return jsonify({"error": "Please select an area of interest."}), 400
    if not time_availability:
        return jsonify({"error": "Please select your time availability."}), 400

    results = filter_projects(skills, level, interest, time_availability)

    if not results:
        return jsonify({
            "message": "No projects matched your inputs. Try selecting different skills or a different interest area.",
            "projects": []
        }), 200

    return jsonify({"projects": results}), 200


@app.route("/project/<int:project_id>")
def project_detail(project_id):
    # Render the full detail page for one project
    project = get_project_by_id(project_id)
    if not project:
        abort(404)
    return render_template("project.html", project=project)


@app.route("/project/<int:project_id>/code")
def view_code(project_id):
    # Return the raw starter code content as JSON for inline viewing
    project = get_project_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found."}), 404

    starter_path = project.get("starter_code", "")
    if not starter_path:
        return jsonify({"error": "No starter code available for this project."}), 404

    filename = os.path.basename(starter_path)
    full_path = os.path.join(STARTER_CODE_DIR, filename)

    if not os.path.exists(full_path):
        return jsonify({"error": "Starter code file not found on server."}), 404

    with open(full_path, "r") as f:
        code_content = f.read()

    return jsonify({"filename": filename, "code": code_content}), 200


@app.route("/project/<int:project_id>/download")
def download_code(project_id):
    # Send the starter code file as a download attachment
    project = get_project_by_id(project_id)
    if not project:
        abort(404)

    starter_path = project.get("starter_code", "")
    if not starter_path:
        abort(404)

    filename = os.path.basename(starter_path)
    full_path = os.path.join(STARTER_CODE_DIR, filename)

    if not os.path.exists(full_path):
        abort(404)

    return send_from_directory(STARTER_CODE_DIR, filename, as_attachment=True)


# ============================================================
# Custom error pages
# ============================================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
