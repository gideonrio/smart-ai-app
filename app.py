import os
import sys
from dotenv import load_dotenv
load_dotenv()
from flask import Flask

# 🚜 Smart AI Farm - Render Deployment Entry Point

# Ensure the subfolder 'Smart-AI-Farm' is in Python's search path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, 'Smart-AI-Farm')
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Clear proxy issues on cloud environments
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)

# Initialize the main app
try:
    from backend.app import create_app
    app = create_app()
except ImportError as e:
    print(f"CRITICAL: Could not import backend.app: {e}")
    # Minimal fallback app for troubleshooting
    app = Flask(__name__)
    @app.route("/")
    def fail():
        return {"error": "Application core missing", "details": "Check logs for import errors"}

# Render expects the object to be named 'app'
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
