from flask import Flask, jsonify
import os
import re

app = Flask(__name__)
LOG_PATH = os.path.join(os.path.dirname(__file__), 'autonomous_run.log')

# Simple log analysis patterns
ERROR_PAT = re.compile(r'(error|fail|exception|traceback|critical)', re.IGNORECASE)
STEP_PATTERNS = [
    (re.compile(r'deep code and config audit', re.I), 'Deep code and config audit'),
    (re.compile(r'automated tests? and deploy verification', re.I), 'Automated test and deploy verification'),
    (re.compile(r'productioniz(e|ing) GUIs? and APIs', re.I), 'Productionize GUIs and APIs'),
    (re.compile(r'deploy(ing)? to cloud', re.I), 'Deploy to cloud and scale agents'),
]

@app.route('/progress.json')
def progress():
    if not os.path.exists(LOG_PATH):
        return jsonify({"step": 0, "logs": [], "errors": [], "insights": ["No log file found."]})
    with open(LOG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()[-200:]
    step = 0
    errors = []
    insights = []
    for line in lines:
        for idx, (pat, _) in enumerate(STEP_PATTERNS, 1):
            if pat.search(line):
                step = max(step, idx)
        if ERROR_PAT.search(line):
            errors.append(line.strip())
    if step == 0:
        insights.append("Waiting for automation to start...")
    elif step < 4:
        insights.append(f"Current step: {STEP_PATTERNS[step-1][1]}")
    else:
        insights.append("All steps completed. Review summary and results.")
    if errors:
        insights.append(f"{len(errors)} error(s) detected. Check details below.")
    return jsonify({
        "step": step,
        "logs": lines[-40:],
        "errors": errors[-10:],
        "insights": insights
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
