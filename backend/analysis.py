FREQUENCY = {
    "Never": 0, "Rarely": 25, "Sometimes": 50, "Frequently": 75, "Daily": 100
}
TIME = {
    "Less than 30 minutes": 10, "30–60 minutes": 35,
    "1–2 hours": 65, "More than 2 hours": 90
}
TOOLS = {
    "1": 25, "2–3": 55, "4–5": 80, "More than 5": 100
}
VERIFICATION = {"Always": 100, "Sometimes": 55, "Rarely": 25, "Never": 0}
LEARNING = {"Yes": 100, "Sometimes": 55, "No": 20}
COPYING = {"Never": 100, "Rarely": 75, "Sometimes": 45, "Often": 10}
PRODUCTIVITY = {"Yes": 100, "Not sure": 55, "No": 25}
DEPENDENCY = {"Low": 20, "Moderate": 55, "High": 90}

def analyze(a):
    usage_score = round(FREQUENCY[a["frequency"]] * 0.6 + TIME[a["daily_time"]] * 0.4)
    learning_score = round(LEARNING[a["learning_use"]] * 0.65 + PRODUCTIVITY[a["productivity"]] * 0.35)
    diversity_score = TOOLS[a["tool_count"]]
    verification_score = VERIFICATION[a["verification"]]
    dependency_score = DEPENDENCY[a["dependency"]]

    if usage_score >= 70:
        usage_level = "High"
    elif usage_score >= 40:
        usage_level = "Moderate"
    else:
        usage_level = "Low"

    if dependency_score >= 75 or (COPYING[a["copying"]] <= 25 and usage_score >= 70):
        category = "AI-Dependent User"
    elif learning_score >= 65 and verification_score >= 50:
        category = "AI-Assisted Learner"
    elif usage_score >= 60:
        category = "Active AI User"
    else:
        category = "Occasional AI User"

    strengths = []
    improvements = []

    if a["purpose"] == "Education / Learning":
        strengths.append("Uses AI primarily for education and learning.")
    elif a["purpose"] == "Coding / Programming":
        strengths.append("Uses AI as a programming or problem-solving support tool.")
    elif a["purpose"] == "Writing / Content":
        strengths.append("Uses AI for writing and content-related tasks.")
    else:
        strengths.append("Uses AI across a practical set of everyday tasks.")

    if verification_score >= 80:
        strengths.append("Usually verifies AI-generated information.")
    else:
        improvements.append("Verify important AI-generated information more consistently.")

    if a["learning_use"] == "Yes":
        strengths.append("Uses AI to understand concepts rather than only obtain answers.")
    else:
        improvements.append("Try using AI to explain concepts step by step instead of only requesting final answers.")

    if a["copying"] in ("Sometimes", "Often"):
        improvements.append("Avoid submitting AI-generated work without understanding or reviewing it.")

    if a["dependency"] == "High":
        improvements.append("Maintain independent problem-solving practice alongside AI use.")

    if a["tool_count"] in ("4–5", "More than 5"):
        strengths.append("Explores multiple AI tools.")
    else:
        improvements.append("Tool diversity is limited; different tools can be useful for different tasks.")

    if not improvements:
        improvements.append("Continue reviewing AI outputs critically and maintaining independent skills.")

    return {
        "usage_score": usage_score,
        "learning_score": learning_score,
        "diversity_score": diversity_score,
        "verification_score": verification_score,
        "dependency_score": dependency_score,
        "usage_level": usage_level,
        "user_category": category,
        "strengths": strengths[:3],
        "improvements": improvements[:3]
    }
