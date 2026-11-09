import os
import socket
from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
REQUESTS = Counter("app_requests_total", "Total requests", ["endpoint"])

@app.route("/")
def index():
    REQUESTS.labels(endpoint="/").inc()
    return jsonify(message="Hello from devops-app",
                   version=os.getenv("APP_VERSION", "dev"),
                   pod=socket.gethostname())

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}