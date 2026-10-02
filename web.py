import os
from flask import Flask, render_template
from dotenv import load_dotenv
import database as db

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "change-me")

@app.route("/")
def index():
    sessions = db.get_all_sessions()
    latest = db.get_latest_session()
    attendance = db.get_attendance(latest["id"]) if latest else []
    return render_template(
        "index.html",
        sessions=sessions,
        latest=latest,
        attendance=attendance
    )

if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=8080, debug=True)
