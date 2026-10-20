from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    """Main endpoint returning application info."""
    return jsonify({
        "message": "Hello from Flask on Kubernetes!",
        "version": "1.0.0",
        "environment": os.getenv("APP_ENV", "development")
    })

@app.route('/health')
def health():
    """Health check endpoint for Kubernetes readiness/liveness probes."""
    return jsonify({
        "status": "healthy",
        "service": "flask-k8s-app"
    }), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
