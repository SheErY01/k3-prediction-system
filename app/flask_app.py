from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "active",
        "service": "K3 Prediction System"
    })

def run_flask_app():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
