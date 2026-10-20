from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import os

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_COUNT = Counter(
    'flask_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'flask_request_duration_seconds',
    'HTTP request duration in seconds',
    ['endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'flask_active_requests',
    'Currently active HTTP requests'
)

APP_INFO = Gauge(
    'flask_app_info',
    'Application information',
    ['version', 'environment']
)
APP_INFO.labels(version='1.0.0', environment=os.getenv('APP_ENV', 'development')).set(1)


@app.before_request
def before_request():
    ACTIVE_REQUESTS.inc()


@app.after_request
def after_request(response):
    ACTIVE_REQUESTS.dec()
    return response


@app.route('/')
def home():
    start = time.time()
    result = jsonify({
        "message": "Monitored Flask App",
        "metrics_endpoint": "/metrics",
        "version": "1.0.0"
    })
    REQUEST_COUNT.labels(method='GET', endpoint='/', status_code=200).inc()
    REQUEST_DURATION.labels(endpoint='/').observe(time.time() - start)
    return result


@app.route('/health')
def health():
    REQUEST_COUNT.labels(method='GET', endpoint='/health', status_code=200).inc()
    return jsonify({"status": "healthy"}), 200


@app.route('/data')
def data():
    """Endpoint that simulates some work for metric demonstration."""
    start = time.time()
    # Simulate a small amount of work
    time.sleep(0.05)
    REQUEST_COUNT.labels(method='GET', endpoint='/data', status_code=200).inc()
    REQUEST_DURATION.labels(endpoint='/data').observe(time.time() - start)
    return jsonify({"data": "sample", "processed": True})


@app.route('/metrics')
def metrics():
    """Expose Prometheus metrics."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
