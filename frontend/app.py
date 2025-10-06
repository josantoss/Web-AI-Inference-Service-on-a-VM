from flask import Flask, render_template, request, jsonify
import os, requests

app = Flask(__name__)
BACKEND_URL = os.environ.get("BACKEND_URL", "http://ai-backend:8000/predict")


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        text = request.form.get("text", "")
        if not text.strip():
            result = {"error": "Empty text"}
        else:
            try:
                resp = requests.post(BACKEND_URL, json={"text": text}, timeout=10)
                result = resp.json()
            except Exception as e:
                result = {"error": f"backend error: {e}"}
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
