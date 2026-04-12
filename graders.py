"""Deterministic grader entrypoint for OpenEnv tasks.

The function accepts flexible payload shapes because different OpenEnv runners
pass slightly different argument names.
"""

from __future__ import annotations

from typing import Any


def _clamp_open_interval(score: float) -> float:
    """Return score clamped to the strict open interval (0, 1)."""
    if score <= 0.0:
        return 0.01
    if score >= 1.0:
        return 0.99
    return float(score)


def _extract(prediction: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = prediction.get(key)
        if value is not None:
            return str(value).strip().lower()
    return ""


def grade_task(*args: Any, **kwargs: Any) -> float:
    """Grade one task episode.

    Supported call patterns include:
    - grade_task(task=..., action=..., info=...)
    - grade_task(task_name=..., prediction=..., reference=...)
    - grade_task({...payload...})
    """
    payload: dict[str, Any] = {}

    if args and isinstance(args[0], dict):
        payload.update(args[0])
    payload.update(kwargs)

    task = str(payload.get("task") or payload.get("task_name") or "").strip().lower()

    action = payload.get("action") or payload.get("prediction") or {}
    if not isinstance(action, dict):
        action = {}

    info = payload.get("info") or payload.get("reference") or payload.get("ground_truth") or {}
    if not isinstance(info, dict):
        info = {}

    predicted_label = _extract(action, "label", "agent_label")
    correct_label = _extract(info, "correct_label", "label", "target_label")
    predicted_response = _extract(action, "response")

    if task == "easy":
        if correct_label and correct_label != "spam":
            correct_label = "not_spam"
        if predicted_label and predicted_label != "spam":
            predicted_label = "not_spam"
        score = 0.8 if predicted_label and predicted_label == correct_label else 0.2
        return _clamp_open_interval(score)

    if task == "medium":
        score = 0.75 if predicted_label and predicted_label == correct_label else 0.25
        return _clamp_open_interval(score)

    if task == "hard":
        classification = 0.6 if predicted_label and predicted_label == correct_label else 0.2
        response_bonus = 0.1

        if correct_label == "important" and any(w in predicted_response for w in ("sure", "will", "attend", "okay", "yes", "confirmed")):
            response_bonus = 0.3
        elif correct_label == "promotion" and any(w in predicted_response for w in ("not interested", "unsubscribe", "no thanks")):
            response_bonus = 0.3
        elif correct_label == "spam" and any(w in predicted_response for w in ("spam", "block", "report", "delete")):
            response_bonus = 0.3

        return _clamp_open_interval(classification + response_bonus)

    # Unknown task or missing data: safe non-boundary score.
    return 0.51