from flask import Flask, jsonify
import os
import socket

app = Flask(__name__)

@app.route('/')
def home():
    """Return pod identity info to demonstrate ReplicaSet distribution."""
    return jsonify({
        "message": "Flask ReplicaSet Demo",
        "pod_name": os.getenv("POD_NAME", socket.gethostname()),
        "pod_ip": os.getenv("POD_IP", "unknown"),
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
