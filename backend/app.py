import os
import time
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from redis import Redis, RedisError

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

load_dotenv(BASE_DIR / ".env")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or None

app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="/")
CORS(app)


def get_redis_client(retries=5, wait=1):
    for i in range(retries):
        try:
            client = Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                password=REDIS_PASSWORD,
                decode_responses=True,
            )
            client.ping()
            return client
        except RedisError:
            if i == retries - 1:
                raise
            time.sleep(wait)


r = get_redis_client()
COUNTER_KEY = "counter:value"
r.set(COUNTER_KEY, 0, nx=True)


@app.get("/api/counter")
def get_counter():
    try:
        return jsonify({"value": int(r.get(COUNTER_KEY) or 0)})
    except Exception:
        return jsonify({"error": "Redis error"}), 500


@app.post("/api/counter/increment")
def increment():
    try:
        return jsonify({"value": r.incr(COUNTER_KEY)})
    except Exception:
        return jsonify({"error": "Redis error"}), 500


@app.post("/api/counter/decrement")
def decrement():
    if int(r.get(COUNTER_KEY)) == 0:
        return jsonify({"error": "Cannot decrement below zero"}), 400
    try:
        return jsonify({"value": r.decr(COUNTER_KEY)})
    except Exception:
        return jsonify({"error": "Redis error"}), 500


@app.post("/api/counter/reset")
def reset():
    try:
        r.set(COUNTER_KEY, 0)
        return jsonify({"value": 0})
    except Exception:
        return jsonify({"error": "Redis error"}), 500


# SPA fallback
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_spa(path):
    if path and (STATIC_DIR / path).exists():
        return send_from_directory(STATIC_DIR, path)
    return send_from_directory(STATIC_DIR, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
