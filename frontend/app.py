from flask import Flask, render_template, request
import os, requests
app = Flask(__name__)

# Use backend service from Docker network or default to local testing
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if not text:
            error = "⚠️ Please enter some text to analyze."
        else:
            try:
                # ---------------------------------------------
                # FIX: Append /predict to the BACKEND_URL
                # ---------------------------------------------
                analysis_url = f"{BACKEND_URL}/predict"
                resp = requests.post(analysis_url, json={"text": text}, timeout=10)
                # ---------------------------------------------
                
                # Check for successful status code (e.g., 200) before parsing JSON
                resp.raise_for_status() 
                result = resp.json()

            except requests.exceptions.HTTPError as e:
                # Handle 4xx or 5xx errors from the backend gracefully
                error = f"❌ Backend Error: {resp.status_code} - {resp.text}"
            except Exception as e:
                error = f"❌ Error connecting to backend: {e}"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)