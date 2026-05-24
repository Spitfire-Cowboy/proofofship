from __future__ import annotations


def _clean_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def profile_url(handle: str, *, base_url: str = "https://proofofship.com") -> str:
    return f"{_clean_base_url(base_url)}/u/{handle}"


def score_url(handle: str, *, base_url: str = "https://proofofship.com") -> str:
    return f"{profile_url(handle, base_url=base_url)}/score.json"


def receipts_url(handle: str, *, base_url: str = "https://proofofship.com") -> str:
    return f"{profile_url(handle, base_url=base_url)}/receipts.json"
