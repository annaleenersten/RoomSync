"""
auth_utils.py
Handles password hashing and authentication helpers.

Sprint 1 Tasks:
- Implement hash_password(password) using SHA-256.
- Implement verify_password(password, hashed) for login.

TEAM OWNER: Jordan (Security & Backend)
"""

import hashlib

def hash_password(password: str) -> str:
    # Jordan
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    # Jordan
    return hashlib.sha256(password.encode()).hexdigest() == hashed