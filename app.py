from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load project data from JSON file
def load_projects():
    with open("data/projects.json", "r") as f:
        return json.load(f)

# Rule-based recommendation system
def recommend_projects(skill, level, interest, time):
    projects = load_projects()
    recommendations = []

    for project in projects:
        if skill in project["skills"] and project["level"].lower() == level.lower():
            if project["interest"].lower() == interest.lower() and project["time"].lower() == time.lower():
                recommendations.append(project)

    # Return top 2–3 projects
    return recommendations[:3]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        skill = request.form.get("skill")
        level = request.form.get("level")
        interest = request.form.get("interest")
        time = request.form.get("time")

        results = recommend_projects(skill, level, interest, time)
        return render_template("index.html", projects=results)

    return render_template("index.html", projects=[])

if __name__ == "__main__":
    app.run(debug=True)
