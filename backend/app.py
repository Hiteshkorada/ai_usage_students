from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, save_response, get_all
from analysis import analyze

app = Flask(__name__)
CORS(app)
init_db()

REQUIRED = [
    "education_level", "frequency", "purpose", "tool_count", "daily_time",
    "verification", "learning_use", "copying", "productivity", "dependency"
]

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "project": "AI Usage Analysis Among Students"})

@app.post("/api/analyze")
def analyze_response():
    answers = request.get_json(silent=True) or {}
    missing = [key for key in REQUIRED if not answers.get(key)]
    if missing:
        return jsonify({"error": "Missing answers", "fields": missing}), 400

    result = analyze(answers)
    record = {**answers, **result}
    record_id = save_response(record)

    return jsonify({"id": record_id, "answers": answers, "analysis": result})

@app.get("/api/stats")
def stats():
    rows = get_all()
    total = len(rows)

    if total == 0:
        return jsonify({
            "total": 0, "education": {}, "purpose": {},
            "usage_levels": {}, "categories": {}, "average_scores": {}
        })

    def counts(field):
        output = {}
        for row in rows:
            value = row[field]
            output[value] = output.get(value, 0) + 1
        return output

    def avg(field):
        return round(sum(row[field] for row in rows) / total, 1)

    return jsonify({
        "total": total,
        "education": counts("education_level"),
        "purpose": counts("purpose"),
        "usage_levels": counts("usage_level"),
        "categories": counts("user_category"),
        "average_scores": {
            "usage": avg("usage_score"),
            "learning": avg("learning_score"),
            "diversity": avg("diversity_score"),
            "verification": avg("verification_score"),
            "dependency": avg("dependency_score")
        }
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
