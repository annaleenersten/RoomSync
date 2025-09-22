"""
database.py
Handles SQLite database connection and queries.

Sprint 1 Tasks:
- Create roommate.db in /data if it doesn’t exist.
- Implement:
  - init_db() → create tables (users, profiles).
  - add_user(email, username, hashed_pw).
  - get_user_by_email(email).
  - add_profile(user_id, budget, location, lifestyle).
  - get_all_profiles() → return all profiles (for matches).

TEAM OWNER: Database 1 (Profiles) & Database 2 (Matches)
"""

import sqlite3

DB_PATH = "../data/roommate.db"

def init_db():
    # Shared: Database 1 + Database 2
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            username TEXT,
            password_hash TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            budget TEXT,
            location TEXT,
            lifestyle TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

def add_user(email, username, hashed_pw):
    # Database 1
    pass

def get_user_by_email(email):
    # Database 1
    pass

def add_profile(user_id, budget, location, lifestyle):
    # Database 1
    pass

def get_all_profiles():
    # Database 2
    return []