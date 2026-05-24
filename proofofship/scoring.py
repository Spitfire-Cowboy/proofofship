from __future__ import annotations

from dataclasses import dataclass
from math import pow
from typing import Iterable


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


def decay_weight(age_days: float, *, half_life_days: float = 90.0) -> float:
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


def contribution(entry: ReceiptInput, *, half_life_days: float = 90.0) -> ReceiptContribution:
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
    """Compute non-decayed (all-time) reputation score."""
    contributions = [contribution(entry) for entry in entries]
    total = sum(item.verification_depth * item.dispute_multiplier for item in contributions)
    return {
        "lifetime_score": total,
        "receipt_count": len(contributions),
    }


def reputation_score(entries: Iterable[ReceiptInput], *, half_life_days: float = 90.0) -> dict:
    breakdown = [contribution(entry, half_life_days=half_life_days) for entry in entries]
    total = sum(item.contribution for item in breakdown)
    all_time = sum(item.verification_depth * item.dispute_multiplier for item in breakdown)
    return {
        "half_life_days": half_life_days,
        "receipt_count": len(breakdown),
        "reputation_score": total,
        "lifetime_score": all_time,
        "breakdown": breakdown,
    }
