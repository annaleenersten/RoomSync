"""
app.py
Main Flask application entry point for Roommate Finder.

Sprint 1 Tasks:
- Set up Flask app and routing.
- Implement routes:
  - '/' → landing page (optional, can redirect to login).
  - '/register' → show registration form and handle account creation.
  - '/login' → show login form and handle authentication.
  - '/profile' → show profile setup page and save preferences.
  - '/matches' → show list of profiles (basic, all users).
- Connect routes to database functions in database.py.
- Use auth_utils.py for password hashing and login checks.

TEAM OWNER: Jordan (Backend & Security)
"""

from flask import Flask, render_template, request, redirect, url_for, session
from auth_utils import hash_password, verify_password
from database import init_db, get_db


app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session management
init_db()

@app.route("/")
def index():
    return redirect(url_for("login"))

# ------------------------
# Jordan – Registration
# ------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = hash_password(request.form["password"])
        db = get_db()
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password))
        db.commit()
        return "User registered!"  # (simple message for now)
    return "Send POST with username & password"

# ------------------------
# Jordan – Login
# ------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if user and verify_password(password, user["password_hash"]):
            return f"Login success for {username}"
        return "Invalid login!"
    return "Send POST with username & password"

@app.route("/profile", methods=["GET", "POST"])
def profile():
    # Database 1 (Profile setup, DB insert)
    if request.method == "POST":
        # TODO: Save profile info
        pass
    return render_template("profile.html")

@app.route("/matches")
def matches():
    # Database 2 (Matches view, DB fetch)
    profiles = []  # TODO: Replace with database.get_all_profiles()
    return render_template("matches.html", profiles=profiles)

if __name__ == "__main__":
    app.run(debug=True)