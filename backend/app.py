from fastapi import FastAPI, Request
from transformers import pipeline
import os

app = FastAPI(title="Sentiment Inference API")
MODEL_NAME = os.environ.get("HF_MODEL", "distilbert-base-uncased-finetuned-sst-2-english")
# load model once at startup
nlp = pipeline("sentiment-analysis", model=MODEL_NAME)

@app.get("/")
def root():
    return {"status": "ok", "model": MODEL_NAME}

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    text = data.get("text", "")
    if not text or not text.strip():
        return {"error": "text field is required"}, 400
    # print("I am analysing the result")
    result = nlp(text)[0]
    print("Now I am done")
    return {"input": text, "label": result["label"], "score": float(result["score"])} ,200
    