from flask import Flask, jsonify, render_template
import os
from app.prediction import predictions_today, daily_stats, results_history

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/predictions')
def get_predictions():
    return jsonify({
        "predictions": predictions_today,
        "stats": daily_stats,
        "results_history": results_history[-10:] if results_history else []
    })

@app.route('/api/stats')
def get_stats():
    return jsonify(daily_stats)

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "active",
        "service": "K3 Prediction System"
    })

def run_flask_app():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
