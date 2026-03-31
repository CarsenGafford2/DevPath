# utils/recommender.py
# Contains all recommendation logic: scoring and filtering projects.
# Kept separate from routing so it can be tested and extended independently.

from utils.data_loader import load_all_projects

# Maximum number of recommendations returned to the user
MAX_RESULTS = 3

# Point weights for each matching criterion
WEIGHT_SKILL   = 3   # Skill matches carry the most influence
WEIGHT_LEVEL   = 2   # Experience level is the next strongest signal
WEIGHT_INTEREST = 2  # Area of interest is equally important as level
WEIGHT_TIME    = 1   # Time availability is a tiebreaker


def parse_skills(skills_string):
    """
    Convert a raw comma-separated skills string into a clean lowercase list.
    Example: "Python, HTML, CSS" -> ["python", "html", "css"]
    """
    return [s.strip().lower() for s in skills_string.split(",") if s.strip()]


def score_single_project(project, user_skills, level, interest, time_availability):
    """
    Calculate a numeric relevance score for one project.

    Each matching criterion adds points:
      - Each matching skill:  +3
      - Level match:          +2
      - Interest match:       +2
      - Time match:           +1

    Returns an integer score (0 means no match at all).
    """
    score = 0

    # Compare user's skills against the project's required skills
    project_skills = [s.lower() for s in project.get("skills", [])]
    matched_skills = sum(1 for skill in user_skills if skill in project_skills)
    score += matched_skills * WEIGHT_SKILL

    # Award points for each additional matching criterion
    if project.get("level", "").lower() == level.lower():
        score += WEIGHT_LEVEL

    if project.get("interest", "").lower() == interest.lower():
        score += WEIGHT_INTEREST

    if project.get("time", "").lower() == time_availability.lower():
        score += WEIGHT_TIME

    return score


def get_recommendations(skills_string, level, interest, time_availability):
    """
    Return the top N recommended projects for the given user inputs.

    Steps:
      1. Parse the raw skills input into a list.
      2. Score every project in the dataset.
      3. Drop projects with a score of zero (no overlap at all).
      4. Sort by score descending.
      5. Return the top MAX_RESULTS projects.
    """
    user_skills = parse_skills(skills_string)
    all_projects = load_all_projects()

    scored_projects = []

    for project in all_projects:
        score = score_single_project(
            project, user_skills, level, interest, time_availability
        )
        if score > 0:
            scored_projects.append({"project": project, "score": score})

    # Sort so the highest-scoring project appears first
    scored_projects.sort(key=lambda item: item["score"], reverse=True)

    # Return only the project dicts, not the score metadata
    return [item["project"] for item in scored_projects[:MAX_RESULTS]]


def validate_recommendation_inputs(skills, level, interest, time_availability):
    """
    Validate all four required fields.
    Returns a list of error strings. An empty list means all inputs are valid.
    """
    errors = []

    if not skills or not skills.strip():
        errors.append("Please enter at least one skill.")

    if not level or not level.strip():
        errors.append("Please select an experience level.")

    if not interest or not interest.strip():
        errors.append("Please select an area of interest.")

    if not time_availability or not time_availability.strip():
        errors.append("Please select your time availability.")

    return errors
