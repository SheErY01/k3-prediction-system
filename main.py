import threading
from app.flask_app import run_flask_app
from app.scheduler import start_scheduler

if __name__ == "__main__":
    threading.Thread(target=run_flask_app, daemon=True).start()
    print("🚀 K3 Prediction System Started")
    start_scheduler()
