from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def required_paths() -> list[Path]:
    return [
        REPO_ROOT / "README.md",
        REPO_ROOT / "LICENSE",
        REPO_ROOT / "CONTRIBUTING.md",
        REPO_ROOT / "SECURITY.md",
        REPO_ROOT / "docs/README.md",
        REPO_ROOT / "docs/concepts.md",
        REPO_ROOT / "docs/global-ledger-contract.md",
        REPO_ROOT / "docs/specs/proofofship-roadmap-v1.md",
        REPO_ROOT / "docs/specs/proofofship-github-auth-and-repo-linking-v1.md",
        REPO_ROOT / "docs/specs/proofofship-repo-badges-v0.md",
        REPO_ROOT / "docs/web/site/index.html",
        REPO_ROOT / "docs/web/site/style.css",
        REPO_ROOT / "docs/web/site/badges/verified.svg",
        REPO_ROOT / "docs/web/site/badges/receipts.svg",
        REPO_ROOT / "docs/web/site/schemas/dr/attestation.v0.1.schema.json",
        REPO_ROOT / "docs/web/site/schemas/dr/transcript.v0.1.schema.json",
        REPO_ROOT / "docs/schemas/proofofship/score.v0.1.schema.json",
        REPO_ROOT / "docs/schemas/proofofship/receipts.v0.1.schema.json",
        REPO_ROOT / "docs/schemas/proofofship/github-account.v0.1.schema.json",
        REPO_ROOT / "docs/schemas/proofofship/linked-repositories.v0.1.schema.json",
        REPO_ROOT / "docs/schemas/proofofship/link-repository-request.v0.1.schema.json",
        REPO_ROOT / "docs/schemas/proofofship/link-repository-result.v0.1.schema.json",
        REPO_ROOT / "examples/score.public.sample.json",
        REPO_ROOT / "examples/receipts.public.sample.json",
        REPO_ROOT / "examples/account.github.public.sample.json",
        REPO_ROOT / "examples/linked-repositories.public.sample.json",
    ]


def missing_required_paths() -> list[str]:
    return [str(path.relative_to(REPO_ROOT)) for path in required_paths() if not path.exists()]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def public_repo_links() -> list[str]:
    texts = [
        (REPO_ROOT / "docs/web/site/index.html").read_text(),
        (REPO_ROOT / "README.md").read_text(),
    ]
    joined = "\n".join(texts)
    links = []
    for needle in [
        "https://github.com/Spitfire-Cowboy/proofofship",
        "https://proofofship.com",
    ]:
        if needle in joined:
            links.append(needle)
    return links


def forbidden_private_strings() -> list[str]:
    forbidden = [
        "gh" + "p_",
        "gh" + "o_",
        "PRIVATE" + " KEY",
        "root@" + "178.156.237.215",
    ]
    hits = []
    for path in REPO_ROOT.rglob("*"):
        if path.is_dir() or ".git" in path.parts or "__pycache__" in path.parts or path.parts[0] in {"tools", "tests"}:
            continue
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue
        for token in forbidden:
            if token in text:
                hits.append(f"{path.relative_to(REPO_ROOT)}:{token}")
    return hits
