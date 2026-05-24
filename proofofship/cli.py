from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from tools.public_repo_checks import missing_required_paths, forbidden_private_strings

from .scoring import ReceiptInput, decay_weight, reputation_score
from .urls import profile_url, receipts_url, score_url


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


def cmd_check_public_surface(args: argparse.Namespace) -> int:
    payload = {
        "missing_required_paths": missing_required_paths(),
        "forbidden_private_strings": forbidden_private_strings(),
    }
    payload["ok"] = not payload["missing_required_paths"] and not payload["forbidden_private_strings"]
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
    score.add_argument("--json", action="store_true")
    score.set_defaults(func=cmd_score)

    urls = sub.add_parser("urls", help="Print canonical public profile URLs for a handle")
    urls.add_argument("handle")
    urls.add_argument("--base-url", default="https://proofofship.com")
    urls.add_argument("--json", action="store_true")
    urls.set_defaults(func=cmd_urls)

    check = sub.add_parser("check-public-surface", help="Run public repo integrity checks")
    check.add_argument("--json", action="store_true")
    check.set_defaults(func=cmd_check_public_surface)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
