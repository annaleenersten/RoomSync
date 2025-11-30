"""
database.py
Handles SQLite database connection and queries.

TEAM OWNER: Database 1 (Profiles) & Database 2 (Matches) (Emery)
"""

import os
import sqlite3

# Get the directory this file lives in
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Build an absolute path to data/roommate.db (inside backend/data)
DB_PATH = os.path.join(BASE_DIR, "data", "roommate.db")

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
            smoking TEXT, 
            pets TEXT,
            cleanliness TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # Matches table to track accepted matches and acceptance time
    c.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user1_id INTEGER NOT NULL,
            user2_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'accepted',
            accepted_at TEXT NOT NULL,
            FOREIGN KEY(user1_id) REFERENCES users(id),
            FOREIGN KEY(user2_id) REFERENCES users(id)
        )
    """)

    # Uniqueness for auth invariants
    c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email)")
    c.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username)")

    conn.commit()
    conn.close()

def add_user(email: str, username: str, hashed_pw: str):
    # Database 1
    """Insert a new user; returns rowid or None on duplicate."""
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (email, username, password_hash)
            VALUES (?, ?, ?)
            """,
            (email, username, hashed_pw),
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return None  # duplicate email or username
    finally:
        conn.close()

def get_user_by_username(username: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? LIMIT 1", (username,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_login(login_identifier: str):
    """Return a user by username OR email."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE username=? OR email=? LIMIT 1",
        (login_identifier, login_identifier),
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

# Helpers for the frontend to access user profile data
def get_profile_by_user_id(user_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM profiles WHERE user_id=? LIMIT 1", (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_and_profile(user_id: int):
    """Username + email + profile fields in one dict."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.id AS user_id, u.username, u.email,
               p.budget, p.location, p.lifestyle, p.smoking, p.pets, p.cleanliness
        FROM users u
        LEFT JOIN profiles p ON p.user_id = u.id
        WHERE u.id=? LIMIT 1
    """, (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_profiles_except(user_id: int):
    """All other users with their profile fields (if any)."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            u.id AS user_id,
            u.username,
            u.email,
            COALESCE(p.budget, '') AS budget,
            COALESCE(p.location, '') AS location,
            COALESCE(p.lifestyle, '') AS lifestyle,
            COALESCE(p.smoking, '') AS smoking,
            COALESCE(p.pets, '') AS pets,
            COALESCE(p.cleanliness, '') AS cleanliness
        FROM users u
        LEFT JOIN profiles p ON p.user_id = u.id
        WHERE u.id <> ?
        ORDER BY u.id
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_user_by_email(email):
    # Database 1
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def add_profile(user_id, budget, location, lifestyle, smoking, pets, cleanliness):
    # Database 1
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO profiles (user_id, budget, location, lifestyle, smoking, pets, cleanliness)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, budget, location, lifestyle, smoking, pets, cleanliness))
    conn.commit()
    conn.close()

def get_all_profiles():
    # Database 2
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM profiles")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# -------------------------
# Matches + cleanup helpers
# -------------------------

def record_accepted_match(user1_id: int, user2_id: int):
    """
    Record that two users have accepted a match.
    Stores timestamp so we can clean up profiles after 10 days.
    """
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO matches (user1_id, user2_id, status, accepted_at)
        VALUES (?, ?, 'accepted', datetime('now'))
    """, (user1_id, user2_id))
    conn.commit()
    conn.close()

def delete_profiles_for_old_matches(days: int = 10):
    """
    Delete profiles for users whose match was accepted at least `days` days ago.
    This satisfies the requirement: delete user profiles 10 days after
    a successful match is accepted.
    """
    conn = get_db()
    cur = conn.cursor()
    # Find all user_ids in accepted matches older than N days
    cur.execute("""
        DELETE FROM profiles
        WHERE user_id IN (
            SELECT user1_id FROM matches
            WHERE status = 'accepted'
              AND accepted_at <= datetime('now', ?)
            UNION
            SELECT user2_id FROM matches
            WHERE status = 'accepted'
              AND accepted_at <= datetime('now', ?)
        )
    """, (f'-{days} days', f'-{days} days'))
    conn.commit()
    conn.close()