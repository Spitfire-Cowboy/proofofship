from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from tools.public_repo_checks import missing_required_paths, forbidden_private_strings, invalid_public_examples, forbidden_site_fallback_links

from .scoring import ReceiptInput, decay_weight, reputation_score
from .urls import profile_url, receipts_url, score_url


def badge_asset_url(kind: str, *, base_url: str) -> str:
    return f"{base_url.rstrip('/')}/badges/{kind}.svg"


def badge_markdown(kind: str, handle: str, *, base_url: str) -> str:
    targets = {
        "verified": profile_url(handle, base_url=base_url),
        "receipts": receipts_url(handle, base_url=base_url),
    }
    labels = {
        "verified": "Verified by Proof of Ship",
        "receipts": "Public receipts available",
    }
    return f"[![{labels[kind]}]({badge_asset_url(kind, base_url=base_url)})]({targets[kind]})"


def _load_receipts_file(path: str | Path) -> list[ReceiptInput]:
    data = json.loads(Path(path).read_text())
    if not isinstance(data, list):
        raise ValueError("receipts file must be a JSON array")
    receipts: list[ReceiptInput] = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("each receipt entry must be a JSON object")
        receipts.append(
            ReceiptInput(
                age_days=item["age_days"],
                verification_depth=item["verification_depth"],
                dispute_multiplier=item.get("dispute_multiplier", 1.0),
                label=item.get("label"),
            )
        )
    return receipts


def cmd_weight(args: argparse.Namespace) -> int:
    payload = {
        "age_days": args.age_days,
        "half_life_days": args.half_life_days,
        "time_weight": decay_weight(args.age_days, half_life_days=args.half_life_days),
    }
    print(json.dumps(payload, indent=2) if args.json else payload["time_weight"])
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    receipts = _load_receipts_file(args.receipts_file)
    result = reputation_score(receipts, half_life_days=args.half_life_days)
    if args.json:
        if args.handle:
            serializable = _public_score_payload(args.handle, result, base_url=args.base_url)
        else:
            serializable = {
                **result,
                "breakdown": [asdict(item) for item in result["breakdown"]],
            }
        print(json.dumps(serializable, indent=2))
        return 0

    print(f"reputation_score={result['reputation_score']:.6f}")
    print(f"lifetime_score={result['lifetime_score']:.6f}")
    print(f"receipt_count={result['receipt_count']}")
    print(f"half_life_days={result['half_life_days']}")
    for index, item in enumerate(result["breakdown"], start=1):
        label = f" label={item.label}" if item.label else ""
        print(
            f"{index}. age_days={item.age_days} depth={item.verification_depth} "
            f"dispute_multiplier={item.dispute_multiplier} time_weight={item.time_weight:.6f} "
            f"contribution={item.contribution:.6f}{label}"
        )
    return 0


def _public_score_payload(handle: str, result: dict, *, base_url: str) -> dict[str, Any]:
    return {
        "handle": handle,
        "reputation_score": result["reputation_score"],
        "lifetime_score": result["lifetime_score"],
        "receipt_count": result["receipt_count"],
        "half_life_days": result["half_life_days"],
        "formula_version": "0.1",
        "profile_url": profile_url(handle, base_url=base_url),
        "score_url": score_url(handle, base_url=base_url),
        "receipts_url": receipts_url(handle, base_url=base_url),
        "breakdown": [asdict(item) for item in result["breakdown"]],
    }


def cmd_receipts(args: argparse.Namespace) -> int:
    receipts = _load_receipts_file(args.receipts_file)
    payload = {
        "handle": args.handle,
        "profile_url": profile_url(args.handle, base_url=args.base_url),
        "receipts_url": receipts_url(args.handle, base_url=args.base_url),
        "receipt_count": len(receipts),
        "receipts": [
            {
                "label": item.label,
                "age_days": item.age_days,
                "verification_depth": item.verification_depth,
                "dispute_multiplier": item.dispute_multiplier,
            }
            for item in receipts
        ],
    }
    print(json.dumps(payload, indent=2) if args.json else payload)
    return 0


def cmd_badge(args: argparse.Namespace) -> int:
    payload: dict[str, Any] = {
        "kind": args.kind,
        "handle": args.handle,
        "badge_url": badge_asset_url(args.kind, base_url=args.base_url),
        "target_url": profile_url(args.handle, base_url=args.base_url) if args.kind == "verified" else receipts_url(args.handle, base_url=args.base_url),
        "markdown": badge_markdown(args.kind, args.handle, base_url=args.base_url),
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(payload["markdown"] if args.markdown else payload["badge_url"])
    return 0


def cmd_urls(args: argparse.Namespace) -> int:
    payload: dict[str, Any] = {
        "profile": profile_url(args.handle, base_url=args.base_url),
        "score": score_url(args.handle, base_url=args.base_url),
        "receipts": receipts_url(args.handle, base_url=args.base_url),
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    payload = {"invalid_public_examples": invalid_public_examples()}
    payload["ok"] = not payload["invalid_public_examples"]
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0 if payload["ok"] else 1


def cmd_check_public_surface(args: argparse.Namespace) -> int:
    payload = {
        "missing_required_paths": missing_required_paths(),
        "forbidden_private_strings": forbidden_private_strings(),
        "invalid_public_examples": invalid_public_examples(),
        "forbidden_site_fallback_links": forbidden_site_fallback_links(),
    }
    payload["ok"] = (
        not payload["missing_required_paths"]
        and not payload["forbidden_private_strings"]
        and not payload["invalid_public_examples"]
        and not payload["forbidden_site_fallback_links"]
    )
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")
    return 0 if payload["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="proofofship",
        description="Public Proof of Ship CLI: score math, URL helpers, and public-surface checks.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    weight = sub.add_parser("weight", help="Compute time decay weight for a receipt age")
    weight.add_argument("age_days", type=float)
    weight.add_argument("--half-life-days", type=float, default=90.0)
    weight.add_argument("--json", action="store_true")
    weight.set_defaults(func=cmd_weight)

    score = sub.add_parser("score", help="Compute a reputation score from a JSON receipts file")
    score.add_argument("receipts_file")
    score.add_argument("--half-life-days", type=float, default=90.0)
    score.add_argument("--handle", default=None, help="Optional handle for public score.json-style output")
    score.add_argument("--base-url", default="https://proofofship.com")
    score.add_argument("--json", action="store_true")
    score.set_defaults(func=cmd_score)

    receipts = sub.add_parser("receipts", help="Render a receipts.json-style payload from a JSON receipts file")
    receipts.add_argument("handle")
    receipts.add_argument("receipts_file")
    receipts.add_argument("--base-url", default="https://proofofship.com")
    receipts.add_argument("--json", action="store_true")
    receipts.set_defaults(func=cmd_receipts)

    badge = sub.add_parser("badge", help="Print badge URL or markdown for a public Proof of Ship badge")
    badge.add_argument("kind", choices=["verified", "receipts"])
    badge.add_argument("handle")
    badge.add_argument("--base-url", default="https://proofofship.com")
    badge.add_argument("--markdown", action="store_true")
    badge.add_argument("--json", action="store_true")
    badge.set_defaults(func=cmd_badge)

    urls = sub.add_parser("urls", help="Print canonical public profile URLs for a handle")
    urls.add_argument("handle")
    urls.add_argument("--base-url", default="https://proofofship.com")
    urls.add_argument("--json", action="store_true")
    urls.set_defaults(func=cmd_urls)

    validate = sub.add_parser("validate", help="Validate checked-in public examples against bundled schemas")
    validate.add_argument("--json", action="store_true")
    validate.set_defaults(func=cmd_validate)

    check = sub.add_parser("check-public-surface", help="Run public repo integrity checks")
    check.add_argument("--json", action="store_true")
    check.set_defaults(func=cmd_check_public_surface)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
