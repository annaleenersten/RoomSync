"""
matching.py
RoomSync – Matching algorithm (standalone, no Flask/DB/UI dependencies)

WHAT THIS MODULE PROVIDES
- compatibility_score(me, other, weights=None) -> int
- rank_candidates(me, candidates, weights=None, top_k=None) -> list[dict]

EXPECTED PROFILE FIELDS (strings OK; normalization is built-in):
{
  "user_id": 123,
  "budget": "800",
  "location": "Seattle",
  "lifestyle": "early sleeper",
  optional extras:
  "smoking": "no",
  "pets": "yes",
  "cleanliness": "medium"
}
"""

from __future__ import annotations
from typing import Any, Iterable, Mapping

DEFAULT_WEIGHTS = {
    "location": 35,
    "budget": 20,
    "lifestyle": 20,
    # Optional extras 
    "smoking": 10,
    "pets": 5,
    "cleanliness": 10,
}

def _norm(s: str | None) -> str:
    if not s:
        return ""
    return " ".join(s.strip().lower().split())

def _budget_bucket(budget: str | None) -> str:
    b = _norm(budget)
    if not b:
        return "unknown"
    digits = "".join(ch for ch in b if ch.isdigit())
    if digits:
        try:
            val = int(digits)
            if val < 700: return "low"
            elif val < 900: return "mid"
            else: return "high"
        except ValueError:
            pass
    if "low" in b: return "low"
    if "mid" in b or "medium" in b: return "mid"
    if "high" in b: return "high"
    return "unknown"

def compatibility_score(
    me: Mapping[str, Any],
    other: Mapping[str, Any],
    weights: dict[str, int] | None = None,
) -> int:
    W = (weights or DEFAULT_WEIGHTS).copy()
    score = 0

    if W.get("location", 0):
        if _norm(me.get("location")) and _norm(other.get("location")):
            if _norm(me.get("location")) == _norm(other.get("location")):
                score += W["location"]

    if W.get("budget", 0):
        if _budget_bucket(me.get("budget")) == _budget_bucket(other.get("budget")):
            score += W["budget"]

    if W.get("lifestyle", 0):
        if _norm(me.get("lifestyle")) and _norm(other.get("lifestyle")):
            if _norm(me.get("lifestyle")) == _norm(other.get("lifestyle")):
                score += W["lifestyle"]

    for key in ("smoking", "pets", "cleanliness"):
        w = W.get(key, 0)
        if w and _norm(me.get(key)) and _norm(other.get(key)):
            if _norm(me.get(key)) == _norm(other.get(key)):
                score += w

    return int(score)

def rank_candidates(
    me: Mapping[str, Any],
    candidates: Iterable[Mapping[str, Any]],
    weights: dict[str, int] | None = None,
    top_k: int | None = None,
) -> list[dict[str, Any]]:
    scored = [{"profile": p, "score": compatibility_score(me, p, weights)} for p in candidates]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k] if top_k else scored