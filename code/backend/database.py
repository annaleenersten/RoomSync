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

TEAM OWNER: Database 1 (Profiles) & Database 2 (Matches) (Emery)
"""

import os
import sqlite3

# Get the directory this file lives in
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Build an absolute path to ../data/roommate.db
DB_PATH = os.path.join(BASE_DIR, "..", "..", "data", "roommate.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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
    conn = sqlite3.connect(DB_PATH)
    try: 
        c= conn.cursor() 
        c.execute("""
            INSERT INTO users (email, username, password_hash)
            VALUES (?, ?, ?)
        """, (email, username, hashed_pw))
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()
    #pass

def get_user_by_email(email):
    # Database 1
    conn = sqlite3.connect(DB_PATH)
    c= conn.cursor() 
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None
    #pass

def add_profile(user_id, budget, location, lifestyle):
    # Database 1
    conn = sqlite3.connect(DB_PATH)
    c= conn.cursor() 
    c.execute("""
        INSERT INTO profiles (user_id, budget, location, lifestyle)
        VALUES (?, ?, ?, ?)
    """, (user_id, budget, location, lifestyle))
    conn.commit()
    conn.close()
    pass

def get_all_profiles():
    # Database 2
    conn = sqlite3.connect(DB_PATH)
    c= conn.cursor() 
    c.execute("SELECT * FROM profiles")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]