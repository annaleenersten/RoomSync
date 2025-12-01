"""
app.py
Main Flask application entry point for Roommate Finder.

TEAM OWNER: Jordan (Backend & Security)
"""

import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from auth_utils import hash_password, verify_password
from database import (
    init_db,
    get_db,
    add_user,
    get_user_by_login,
    get_user_by_username,
    get_user_and_profile,
    get_profiles_except,
    record_accepted_match,
    delete_profiles_for_old_matches,
)
import database as db
from matching import rank_candidates

# ---- Tell Flask where templates/static actually are ----
APP_DIR = os.path.dirname(os.path.abspath(__file__))          # code/backend
TEMPLATE_DIR = os.path.join(APP_DIR, "..", "frontend", "templates")
STATIC_DIR   = os.path.join(APP_DIR, "..", "frontend", "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

app.secret_key = os.environ.get("FLASK_SECRET", "supersecretkey")  # Needed for session management
init_db()

@app.route("/")
def index():
    return redirect(url_for("base"))

@app.route("/base")
def base():
    return render_template("base.html")

# ---------------------------------------------------
# Jordan – Registration (email + username + password)
# ---------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message=None)

    email = (request.form.get("email") or "").strip().lower()
    username = (request.form.get("username") or "").strip()
    password_raw = (request.form.get("password") or "").strip()

    if not (email and username and password_raw):
        return render_template("register.html", message="Please provide email, username, and password.")

    db = get_db()
    existing = db.execute("SELECT 1 FROM users WHERE email=? OR username=?", (email, username)).fetchone()
    if existing:
        return render_template("register.html", message="Email or username already exists.")

    db.execute(
        "INSERT INTO users (email, username, password_hash) VALUES (?, ?, ?)",
        (email, username, hash_password(password_raw)),
    )
    db.commit()
    return redirect(url_for("login"))

# ----------------------------------
# Jordan – Login (username)
# ----------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", message=None)

    username = (request.form.get("username") or "").strip()
    password = (request.form.get("password") or "").strip()

    if not username or not password:
        return render_template("login.html", message="Please enter username and password.")

    user = get_user_by_username(username)
    if user and verify_password(password, user["password_hash"]):
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("matches"))

    return render_template("login.html", message="Invalid login credentials.")

#---------------------
# Joe - Update Preferences
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    user_id = session["user_id"]
    message = None

    if request.method == "POST":
        # Get form values safely and strip whitespace
        budget = (request.form.get("budget") or "").strip()
        location = (request.form.get("location") or "").strip()
        lifestyle = (request.form.get("lifestyle") or "").strip()
        smoking = (request.form.get("smoking") or "").strip()
        pets = (request.form.get("pets") or "").strip()
        cleanliness = (request.form.get("cleanliness") or "").strip()

        # Check if profile exists
        profile_exists = db.execute(
            "SELECT 1 FROM profiles WHERE user_id=?",
            (user_id,)
        ).fetchone()

        if profile_exists:
            # Update existing record
            db.execute("""
                UPDATE profiles
                SET budget=?, location=?, lifestyle=?, smoking=?, pets=?, cleanliness=?
                WHERE user_id=?
            """, (budget, location, lifestyle, smoking, pets, cleanliness, user_id))
        else:
            # Insert new record
            db.execute("""
                INSERT INTO profiles (user_id, budget, location, lifestyle, smoking, pets, cleanliness)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, budget, location, lifestyle, smoking, pets, cleanliness))

        db.commit()
        message = "Profile updated successfully."

    # Fetch updated profile to display
    profile_row = get_user_and_profile(user_id)
    return render_template("profile.html", message=message, profile=profile_row)

# ----------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/matches")
def matches():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    me = get_user_and_profile(user_id)
    candidates = get_profiles_except(user_id) or []
    ranked = []

    # Only rank if there are candidates
    if candidates:
        ranked = rank_candidates(me, candidates)
    else:
        # Avoid template crash if no matches exist
        candidates = [{"username": "No matches yet"}]
        ranked = [{"profile": {"username": "No matches yet", "location": "", "budget": "", "lifestyle": ""}, "score": 0}]

    return render_template("matches.html", ranked=ranked, profiles=candidates)

# ----------------------------------
# Accept a match and trigger cleanup
# ----------------------------------
@app.route("/matches/accept/<int:other_id>", methods=["POST"])
def accept_match(other_id):
    """
    Called when the current user accepts a match with another user.
    Records the accepted match and runs profile cleanup for matches
    older than 10 days.
    """
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    # Record the accepted match (user_id <-> other_id)
    record_accepted_match(user_id, other_id)

    # Run cleanup to delete profiles for any matches accepted 10+ days ago
    delete_profiles_for_old_matches(days=10)

    return redirect(url_for("matches"))

@app.route("/admin/users")
def admin_users():
    # Also run cleanup here so admins always see a "fresh" system
    delete_profiles_for_old_matches(days=10)

    db = get_db()
    rows = db.execute("SELECT id, email, username FROM users ORDER BY id").fetchall()
    html = ["<h3>All Users</h3><table border='1' cellpadding='6'>",
            "<tr><th>ID</th><th>Email</th><th>Username</th></tr>"]
    for r in rows:
        html.append(f"<tr><td>{r['id']}</td><td>{r['email']}</td><td>{r['username']}</td></tr>")
    html.append("</table>")
    return "".join(html)
# ----------------------------------

# --------------------------------------------------
# Joe – Block & Report user
# --------------------------------------------------
@app.route("/block", methods=["POST"])
def block_user_route():
    data = request.json
    blocker_id = data.get("blocker_id")
    blocked_id = data.get("blocked_id")

    if not blocker_id or not blocked_id:
        return jsonify({"error": "Missing blocker_id or blocked_id"}), 400

    db.block_user(blocker_id, blocked_id)
    return jsonify({"message": "User blocked successfully"})


@app.route("/report", methods=["POST"])
def report_user_route():
    data = request.json
    reporter_id = data.get("reporter_id")
    reported_id = data.get("reported_id")
    reason = data.get("reason", "")

    if not reporter_id or not reported_id:
        return jsonify({"error": "Missing reporter_id or reported_id"}), 400

    db.report_user(reporter_id, reported_id, reason)
    return jsonify({"message": "User reported successfully"})

# ----------------------------------


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)), debug=False)