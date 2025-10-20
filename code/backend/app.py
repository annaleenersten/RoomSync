"""
app.py
Main Flask application entry point for Roommate Finder.

TEAM OWNER: Jordan (Backend & Security)
"""

import os
from flask import Flask, render_template, request, redirect, url_for, session
from auth_utils import hash_password, verify_password
from database import init_db, get_db, add_user, get_user_by_login, get_user_by_username, get_user_and_profile, get_profiles_except
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
    user_id = session["user_id"] # Gets userID
    message = None

    # Only run if user submits form. Takes values that user inputted.
    if request.method == "POST":
        budget    = request.form.get("budget", "")
        location  = request.form.get("location", "")
        lifestyle = request.form.get("lifestyle", "")

        #Gets row of data with userID
        existing = db.execute("SELECT * FROM profiles WHERE user_id=?", (user_id,)).fetchone()

        if existing: # If user already has profile, update values
            db.execute("""
                UPDATE profiles
                SET budget=?, location=?, lifestyle=?
                WHERE user_id=?
            """, (budget, location, lifestyle, user_id))
        else: # Otherwise, create a new profile row to user
            db.execute("INSERT INTO profiles (user_id, budget, location, lifestyle) VALUES (?, ?, ?, ?)",
                       (user_id, budget, location, lifestyle))

        db.commit()
        # If successfully changed, return this message to reflect that
        message = "Profile updated."

    profile_row = get_user_and_profile(user_id)  # username/email + profile fields
    return render_template("profile.html", message=message, profile=profile_row)


# ----------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/matches")
def matches():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    me = get_user_and_profile(user_id) or {}
    candidates = get_profiles_except(user_id)

    matches_flat = candidates
    ranked_list = rank_candidates(me, candidates)

    return render_template("matches.html", profiles=matches_flat, ranked=ranked_list)

@app.route("/admin/users")
def admin_users():
    db = get_db()
    rows = db.execute("SELECT id, email, username FROM users ORDER BY id").fetchall()
    html = ["<h3>All Users</h3><table border='1' cellpadding='6'>",
            "<tr><th>ID</th><th>Email</th><th>Username</th></tr>"]
    for r in rows:
        html.append(f"<tr><td>{r['id']}</td><td>{r['email']}</td><td>{r['username']}</td></tr>")
    html.append("</table>")
    return "".join(html)
# ----------------------------------

if __name__ == "__main__":
    app.run(debug=True)
