from flask import Flask, jsonify
import os 
app = Flask(__name__)

# Simulating an application state
is_ready = os.getenv("IS_READY")
is_started = os.getenv("IS_STARTED")

@app.route('/health', methods=['GET'])
def health_check():
    """Liveness probe - always returns 200 if the app is running"""
    return jsonify(status="Healthy"), 200

@app.route('/ready', methods=['GET'])
def readiness_check():
    """Readiness probe - returns 200 only if the app is ready"""
    global is_ready
    if is_ready:
        return jsonify(status="Ready"), 200
    return jsonify(status="Not Ready"), 503  # Service Unavailable

@app.route('/startup', methods=['GET'])
def startup_check():
    """Startup probe - returns 200 only after startup is complete"""
    global is_started
    if is_started:
        return jsonify(status="Started"), 200
    return jsonify(status="Starting"), 503  # Service Unavailable

# Simulate application startup process
import threading
import time

def simulate_startup():
    global is_started, is_ready
    time.sleep(10)  # Simulating a long startup time
    is_started = True
    time.sleep(5)   # Additional time before app is fully ready
    is_ready = True

threading.Thread(target=simulate_startup).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
