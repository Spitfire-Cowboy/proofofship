from __future__ import annotations

from dataclasses import dataclass
from math import pow
from typing import Iterable


HUMAN_RECENT_ACTIVITY_HALF_LIFE_DAYS = 365.0
NON_HUMAN_RECENT_ACTIVITY_HALF_LIFE_DAYS = 90.0


@dataclass(slots=True)
class ReceiptInput:
    age_days: float
    verification_depth: float
    dispute_multiplier: float = 1.0
    label: str | None = None


@dataclass(slots=True)
class ReceiptContribution:
    age_days: float
    verification_depth: float
    dispute_multiplier: float
    time_weight: float
    contribution: float
    label: str | None = None


def default_recent_activity_half_life_days(actor_kind: str = "human") -> float:
    normalized = (actor_kind or "human").strip().lower()
    if normalized == "human":
        return HUMAN_RECENT_ACTIVITY_HALF_LIFE_DAYS
    if normalized in {"agent", "bot", "org", "organization"}:
        return NON_HUMAN_RECENT_ACTIVITY_HALF_LIFE_DAYS
    raise ValueError(f"unknown actor_kind: {actor_kind!r}")


def decay_weight(age_days: float, *, half_life_days: float = NON_HUMAN_RECENT_ACTIVITY_HALF_LIFE_DAYS) -> float:
    if half_life_days <= 0:
        raise ValueError("half_life_days must be positive")
    if age_days < 0:
        raise ValueError("age_days cannot be negative")
    return pow(2.0, -(age_days / half_life_days))


def _validated_depth(depth: float) -> float:
    if depth < 0.0 or depth > 1.0:
        raise ValueError("verification_depth must be between 0.0 and 1.0")
    return depth


def _validated_dispute(multiplier: float) -> float:
    if multiplier < 0.0 or multiplier > 1.0:
        raise ValueError("dispute_multiplier must be between 0.0 and 1.0")
    return multiplier


def contribution(entry: ReceiptInput, *, half_life_days: float) -> ReceiptContribution:
    depth = _validated_depth(float(entry.verification_depth))
    dispute_multiplier = _validated_dispute(float(entry.dispute_multiplier))
    weight = decay_weight(float(entry.age_days), half_life_days=half_life_days)
    value = weight * depth * dispute_multiplier
    return ReceiptContribution(
        age_days=float(entry.age_days),
        verification_depth=depth,
        dispute_multiplier=dispute_multiplier,
        time_weight=weight,
        contribution=value,
        label=entry.label,
    )


def lifetime_score(entries: Iterable[ReceiptInput]) -> dict:
    rows = list(entries)
    total = sum(
        _validated_depth(float(entry.verification_depth)) * _validated_dispute(float(entry.dispute_multiplier))
        for entry in rows
    )
    return {
        "lifetime_score": total,
        "receipt_count": len(rows),
    }


def reputation_score(
    entries: Iterable[ReceiptInput], *, recent_activity_half_life_days: float | None = None, actor_kind: str = "human"
) -> dict:
    normalized_actor_kind = (actor_kind or "human").strip().lower()
    effective_half_life_days = float(
        recent_activity_half_life_days
        if recent_activity_half_life_days is not None
        else default_recent_activity_half_life_days(normalized_actor_kind)
    )
    breakdown = [contribution(entry, half_life_days=effective_half_life_days) for entry in entries]
    recent_total = sum(item.contribution for item in breakdown)
    lifetime_total = sum(item.verification_depth * item.dispute_multiplier for item in breakdown)
    public_reputation = lifetime_total if normalized_actor_kind == "human" else recent_total
    return {
        "actor_kind": normalized_actor_kind,
        "reputation_score": public_reputation,
        "lifetime_score": lifetime_total,
        "recent_activity_score": recent_total,
        "recent_activity_half_life_days": effective_half_life_days,
        "receipt_count": len(breakdown),
        "breakdown": breakdown,
    }
