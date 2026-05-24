from __future__ import annotations

from pathlib import Path

from tools.public_repo_checks import (
    REPO_ROOT,
    forbidden_private_strings,
    invalid_public_examples,
    load_json,
    missing_required_paths,
    public_repo_links,
    forbidden_site_fallback_links,
)


def test_required_paths_exist():
    assert missing_required_paths() == []


def test_public_site_links_point_to_public_repo_and_domain():
    links = public_repo_links()
    assert "https://github.com/Spitfire-Cowboy/proofofship" in links
    assert "https://proofofship.com" in links


def test_schema_files_parse_as_json():
    for rel in [
        "docs/web/site/schemas/dr/attestation.v0.1.schema.json",
        "docs/web/site/schemas/dr/transcript.v0.1.schema.json",
        "docs/schemas/proofofship/score.v0.1.schema.json",
        "docs/schemas/proofofship/receipts.v0.1.schema.json",
        "docs/schemas/proofofship/github-account.v0.1.schema.json",
        "docs/schemas/proofofship/linked-repositories.v0.1.schema.json",
        "docs/schemas/proofofship/link-repository-request.v0.1.schema.json",
        "docs/schemas/proofofship/link-repository-result.v0.1.schema.json",
    ]:
        data = load_json(REPO_ROOT / rel)
        assert isinstance(data, dict)
        assert "$schema" in data
        assert "title" in data


def test_public_examples_parse_as_json():
    for rel in [
        "examples/score.public.sample.json",
        "examples/receipts.public.sample.json",
        "examples/account.github.public.sample.json",
        "examples/linked-repositories.public.sample.json",
        "examples/link-repository-request.public.sample.json",
        "examples/link-repository-result.public.sample.json",
    ]:
        data = load_json(REPO_ROOT / rel)
        assert isinstance(data, dict)


def test_no_obvious_private_strings_leak_into_public_repo():
    hits = forbidden_private_strings()
    assert hits == []


def test_public_examples_validate_against_schemas():
    assert invalid_public_examples() == []


def test_docs_site_does_not_fall_back_to_github_for_core_docs():
    assert forbidden_site_fallback_links() == []
