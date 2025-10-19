"""
matching.py
Matching algorithm (standalone)

Public API:
- compatibility_score(me, other, weights=None) -> int
- rank_candidates(me, candidates, weights=None, top_k=None, min_required_keys=None) -> list[dict]
"""

from __future__ import annotations
from typing import Any, Iterable, Mapping, Sequence

DEFAULT_WEIGHTS = {
    "location": 40,
    "budget": 30,
    "lifestyle": 30,
    # Optional extras:
    # "smoking": 15,
    # "pets": 10,
    # "cleanliness": 10,
}

# --------- helpers ---------

def _norm(s: str | None) -> str:
    if not s:
        return ""
    return " ".join(str(s).strip().lower().split())

def _to_number(value: Any) -> float | None:
    """Extract first numeric token from a messy string like '$900/mo' -> 900."""
    if value is None:
        return None
    s = str(value)
    digits = "".join(ch for ch in s if (ch.isdigit() or ch == "."))
    if digits and digits != ".":
        try:
            return float(digits)
        except ValueError:
            return None
    return None

def _budget_bucket(budget: Any) -> str:
    """
    Coarse budget bucketing (tune ranges later).
      low: < 700
      mid: 700–899
      high: >= 900
    Falls back to keywords if no number is found.
    """
    n = _to_number(budget)
    if n is not None:
        if n < 700:
            return "low"
        elif n < 900:
            return "mid"
        else:
            return "high"

    b = _norm(str(budget) if budget is not None else "")
    if not b:
        return "unknown"
    if "low" in b:
        return "low"
    if "mid" in b or "medium" in b:
        return "mid"
    if "high" in b:
        return "high"
    return "unknown"

def _effective_weights(weights: dict[str, int] | None) -> dict[str, float]:
    """Normalize weights to sum to 100 (for easier reasoning)."""
    W = (weights or DEFAULT_WEIGHTS).copy()
    total = sum(max(v, 0) for v in W.values()) or 1
    return {k: (max(v, 0) * 100.0 / total) for k, v in W.items()}

# --------- scoring ---------

def compatibility_score(
    me: Mapping[str, Any],
    other: Mapping[str, Any],
    weights: dict[str, int] | None = None,
) -> int:
    """
    Compute a compatibility score using a weighted sum of criterion matches.
    - location: exact normalized match
    - budget: bucket match (low/mid/high/unknown)
    - lifestyle: exact normalized match
    Optional extras (if present in weights): smoking, pets, cleanliness
    """
    W = _effective_weights(weights)
    score = 0.0

    # Location (exact match)
    mloc, oloc = _norm(me.get("location")), _norm(other.get("location"))
    if mloc and oloc and mloc == oloc:
        score += W.get("location", 0)

    # Budget (bucket match)
    if _budget_bucket(me.get("budget")) == _budget_bucket(other.get("budget")):
        score += W.get("budget", 0)

    # Lifestyle (exact match)
    mlife, olife = _norm(me.get("lifestyle")), _norm(other.get("lifestyle"))
    if mlife and olife and mlife == olife:
        score += W.get("lifestyle", 0)

    # Optional extras
    for key in ("smoking", "pets", "cleanliness"):
        if key in W:
            mv, ov = _norm(me.get(key)), _norm(other.get(key))
            if mv and ov and mv == ov:
                score += W[key]

    return int(round(score))

def rank_candidates(
    me: Mapping[str, Any],
    candidates: Iterable[Mapping[str, Any]],
    weights: dict[str, int] | None = None,
    top_k: int | None = None,
    min_required_keys: Sequence[str] | None = None,
) -> list[dict[str, Any]]:
    """
    Rank candidates by compatibility (highest first).
    Returns: [{"profile": <candidate>, "score": <int>}, ...]
    - min_required_keys: if provided, skip candidates that lack any of these fields.
    - tie-breaker: stable by username/user_id if available to avoid jitter.
    """
    def has_required(p: Mapping[str, Any]) -> bool:
        if not min_required_keys:
            return True
        return all(_norm(p.get(k)) != "" for k in min_required_keys)

    filtered = [p for p in candidates if has_required(p)]
    scored = [{"profile": p, "score": compatibility_score(me, p, weights)} for p in filtered]

    def tiebreak(item: dict) -> tuple:
        p = item["profile"]
        # Prefer stable id/name if present; fallback to string of dict
        return (
            -item["score"],
            _norm(p.get("username")) or str(p.get("user_id") or ""),
            str(p),
        )

    scored.sort(key=tiebreak)
    return scored[:top_k] if top_k else scored