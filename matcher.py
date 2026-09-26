def classify_college(student_sat, gpa, sat_25, sat_75, admission_rate):
    """Return a simple college match category based on historical data."""
    # GPA guardrail: a very low GPA should not be presented as a realistic match.
    if gpa < 2.0:
        return "Reach"

    # Highly selective colleges remain reaches in this simple model.
    if admission_rate < 0.15:
        return "Reach"

    # GPA and SAT both participate in the match.
    if student_sat >= sat_75 and gpa >= 3.5:
        return "Likely"

    if student_sat >= sat_25 and gpa >= 3.0:
        return "Target"

    return "Reach"


def profile_bonus(gpa, extracurriculars, leadership, volunteering):
    """Create a small profile score used only as supporting context."""
    score = 0

    if gpa >= 3.7:
        score += 2
    elif gpa >= 3.3:
        score += 1

    if extracurriculars == "Strong":
        score += 2
    elif extracurriculars == "Moderate":
        score += 1

    if leadership:
        score += 1

    if volunteering:
        score += 1

    return score
