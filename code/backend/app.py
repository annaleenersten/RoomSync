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

from flask import Flask, render_template, request, redirect, url_for
import database
import auth_utils

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    # Jordan (with database support from Database 1)
    if request.method == "POST":
        # TODO: Handle registration logic
        pass
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # Jordan (login/authentication logic)
    if request.method == "POST":
        # TODO: Handle login logic
        pass
    return render_template("login.html")

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