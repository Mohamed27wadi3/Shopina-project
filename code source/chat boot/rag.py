from sentence_transformers import SentenceTransformer
import json, os, requests, numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify,render_template

from pathlib import Path

knowledge_path = Path(__file__).resolve().parent / "knowledge.json"
if knowledge_path.exists():
    with open(knowledge_path, "r", encoding="utf-8") as f:
        knowledge = json.load(f)
else:
    knowledge = []

model = SentenceTransformer("all-MiniLM-L6-v2")
docs = [f"{item.get('title', '')}: {item.get('content', '')}" for item in knowledge]
doc_embedding = model.encode(docs) if docs else []

def retrieve_context(query, k=2):
    query_embedding = model.encode([query])
    if not docs:
        return ""
    similarity = cosine_similarity(query_embedding, doc_embedding)[0]
    top_indices = np.argsort(similarity)[-k:][::-1]
    top_docs = [docs[i] for i in top_indices]
    return "\n".join(top_docs)

app = Flask(__name__)
GEMENI_API_KEY = os.environ.get("CHATBOT_GEMINI_API_KEY")
@app.route("/")
def home():
    return render_template("cc.html")

chat_history = []
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("message", "")
    if not query:
        return jsonify({"error": "Missing message"}), 400

    # 1. Add the user's message to history
    chat_history.append({
        "role": "user",
        "parts": [{"text": query}]
    })

    # 2. Get context and build the prompt
    context = retrieve_context(query)
    full_prompt = f"{context}\n\nUser question: {query}"

    # 3. Add prompt to history and call Gemini
    if not GEMENI_API_KEY:
        return jsonify({"error": "Missing API key"}), 500

    API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMENI_API_KEY}"
    payload = {
        "contents": chat_history + [{"role": "user", "parts": [{"text": full_prompt}]}]
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, headers=headers, json=payload)

    if not response.ok:
        return jsonify({"error": response.json().get("error", {})}), 500

    reply = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

    # 4. Add the model's response to history
    chat_history.append({
        "role": "model",
        "parts": [{"text": reply}]
    })

    return jsonify({"response": reply})


if __name__ == '__main__':
    app.run(debug=True)
