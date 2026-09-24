def classify_college(student_sat, sat_25, sat_75, admission_rate):
    """Return a simple college match category based on historical data."""
    if admission_rate < 0.15:
        return "Reach"

    if student_sat >= sat_75:
        return "Likely"

    if student_sat >= sat_25:
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
