from flask import Flask, jsonify
import redis
import mysql.connector
import os
import time

app = Flask(__name__)

def get_redis():
    """Get Redis connection with retry."""
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True
    )

def get_db():
    """Get MySQL connection."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql"),
        user=os.getenv("DB_USER", "devops"),
        password=os.getenv("DB_PASSWORD", "devops123"),
        database=os.getenv("DB_NAME", "devopsdb"),
        connection_timeout=5
    )

@app.route('/')
def home():
    """Main endpoint demonstrating Redis counter and MySQL connectivity."""
    # Redis counter
    try:
        r = get_redis()
        visit_count = r.incr("visit_count")
        redis_status = "connected"
    except Exception as e:
        visit_count = -1
        redis_status = f"error: {str(e)}"

    # MySQL check
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        db_version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        db_status = f"connected (MySQL {db_version})"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return jsonify({
        "message": "Docker Networking Demo",
        "visit_count": visit_count,
        "redis": redis_status,
        "database": db_status
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
