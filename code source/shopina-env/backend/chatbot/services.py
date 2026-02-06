import json
import re
from functools import lru_cache
from pathlib import Path
from typing import List, Tuple

import numpy as np
import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.html import escape
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MAX_MESSAGE_LENGTH = getattr(settings, 'CHATBOT_MAX_MESSAGE_LENGTH', 1000)
RATE_LIMIT_PER_MIN = getattr(settings, 'CHATBOT_RATE_LIMIT_PER_MINUTE', 20)
GEMINI_MODEL = getattr(settings, 'CHATBOT_GEMINI_MODEL', 'gemini-2.0-flash')


def sanitize_text(text: str) -> str:
    if not text:
        return ''
    cleaned = text.strip()
    cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', ' ', cleaned)
    cleaned = cleaned.replace('\u202e', '').replace('\u202d', '')
    cleaned = cleaned[:MAX_MESSAGE_LENGTH]
    return cleaned


def rate_limited(key: str) -> bool:
    cache_key = f"chatbot:rate:{key}"
    try:
        count = cache.incr(cache_key)
    except ValueError:
        cache.set(cache_key, 1, timeout=60)
        count = 1
    return count > RATE_LIMIT_PER_MIN


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    return SentenceTransformer('all-MiniLM-L6-v2')


@lru_cache(maxsize=1)
def _load_knowledge() -> Tuple[List[str], np.ndarray | None]:
    base_dir = Path(getattr(settings, 'CHATBOT_DIR', '')).resolve()
    knowledge_path = base_dir / 'knowledge.json'
    if not knowledge_path.exists():
        return [], None

    with open(knowledge_path, 'r', encoding='utf-8') as f:
        knowledge = json.load(f)

    docs = [f"{item.get('title', '')}: {item.get('content', '')}" for item in knowledge]
    if not docs:
        return [], None

    model = _get_model()
    embeddings = model.encode(docs)
    return docs, embeddings


def _retrieve_context(query: str, k: int = 2) -> str:
    docs, embeddings = _load_knowledge()
    if not docs or embeddings is None:
        return ''

    model = _get_model()
    query_embedding = model.encode([query])
    similarity = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = np.argsort(similarity)[-k:][::-1]
    top_docs = [docs[i] for i in top_indices]
    return "\n".join(top_docs)


def build_prompt(role: str, query: str) -> str:
    context = _retrieve_context(query)
    role_hint = f"User role: {role}"
    if context:
        return f"{role_hint}\n\nContext:\n{context}\n\nUser question: {query}"
    return f"{role_hint}\n\nUser question: {query}"


def call_gemini(messages: List[dict]) -> str:
    api_key = getattr(settings, 'CHATBOT_GEMINI_API_KEY', None)
    if not api_key or api_key.startswith('Demo') or api_key.startswith('your_'):
        # Fallback mode: respond with knowledge base when API key is not configured
        return "Bienvenue! Je suis l'assistant Shopina. Vous pouvez me poser des questions sur la plateforme, comment créer une boutique, les options de paiement, etc. Comment puis-je vous aider?"

    api_url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={api_key}"
    )

    payload = {
        "contents": messages,
    }

    try:
        response = requests.post(api_url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
        if not response.ok:
            # Fallback on API error
            return "Bienvenue! Je suis l'assistant Shopina. Comment puis-je vous aider?"

        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"[Chatbot Error] {e}")
        # Fallback on any error
        return "Bienvenue! Je suis l'assistant Shopina. Comment puis-je vous aider?"


def get_history(cache_key: str) -> List[dict]:
    return cache.get(cache_key, [])


def save_history(cache_key: str, history: List[dict]) -> None:
    cache.set(cache_key, history, timeout=60 * 60)


def append_history(cache_key: str, role: str, text: str) -> List[dict]:
    history = get_history(cache_key)
    history.append({"role": role, "parts": [{"text": text}]})
    save_history(cache_key, history)
    return history


def build_cache_key(user_id: int | None, session_key: str | None) -> str:
    if user_id:
        return f"chatbot:user:{user_id}"
    return f"chatbot:session:{session_key or 'guest'}"


def build_response(query: str, role: str, cache_key: str) -> str:
    safe_query = sanitize_text(query)
    safe_query = escape(safe_query)

    history = append_history(cache_key, "user", safe_query)
    prompt = build_prompt(role, safe_query)
    messages = history + [{"role": "user", "parts": [{"text": prompt}]}]

    reply = call_gemini(messages)
    safe_reply = escape(reply)
    append_history(cache_key, "model", safe_reply)
    return safe_reply
