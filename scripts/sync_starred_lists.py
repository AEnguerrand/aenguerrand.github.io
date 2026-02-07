#!/usr/bin/env python3
"""Fetch GitHub stars and build grouped data from a local mapping file."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen


DEFAULT_MAPPING_PATH = Path("data/starred-lists.json")
DEFAULT_OUTPUT_PATH = Path("public/data/starred-groups.json")
API_VERSION = "2022-11-28"
PER_PAGE = 100


def load_json_file(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def request_json(url: str, token: str | None) -> Any:
    headers = {
        "Accept": "application/vnd.github.star+json",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "starred-lists-sync-script",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(url, headers=headers)
    with urlopen(request) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


def normalize_repo(item: dict[str, Any]) -> dict[str, Any]:
    if "repo" in item:
        repo_data = item["repo"]
        starred_at = item.get("starred_at")
    else:
        repo_data = item
        starred_at = None

    topics = repo_data.get("topics") or []
    if not isinstance(topics, list):
        topics = []

    return {
        "id": repo_data["id"],
        "full_name": repo_data["full_name"],
        "html_url": repo_data["html_url"],
        "description": repo_data.get("description"),
        "stargazers_count": repo_data.get("stargazers_count", 0),
        "forks_count": repo_data.get("forks_count", 0),
        "language": repo_data.get("language"),
        "archived": bool(repo_data.get("archived", False)),
        "fork": bool(repo_data.get("fork", False)),
        "topics": [str(topic) for topic in topics],
        "updated_at": repo_data.get("updated_at"),
        "starred_at": starred_at,
    }


def fetch_all_starred_repos(username: str, token: str | None) -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    page = 1

    while True:
        url = (
            f"https://api.github.com/users/{quote(username)}/starred"
            f"?per_page={PER_PAGE}&page={page}&sort=created&direction=desc"
        )
        payload = request_json(url, token)

        if not isinstance(payload, list):
            raise RuntimeError("Unexpected GitHub API response format.")

        if not payload:
            break

        repos.extend(normalize_repo(item) for item in payload if isinstance(item, dict))

        if len(payload) < PER_PAGE:
            break

        page += 1

    return repos


def build_grouped_dataset(mapping: dict[str, Any], starred_repos: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    username = mapping.get("username")
    if not isinstance(username, str) or not username:
        raise ValueError("Mapping file must define a non-empty 'username'.")

    configured_lists = mapping.get("lists")
    if not isinstance(configured_lists, list):
        raise ValueError("Mapping file must define 'lists' as an array.")

    unlisted = mapping.get("unlisted") or {}
    if not isinstance(unlisted, dict):
        raise ValueError("'unlisted' must be an object when provided.")

    unlisted_slug = str(unlisted.get("slug") or "to-classify")
    unlisted_group = {
        "slug": unlisted_slug,
        "name": str(unlisted.get("name") or "To Classify"),
        "description": str(unlisted.get("description") or "New stars not assigned to a list yet."),
        "repos": [],
    }

    groups: dict[str, dict[str, Any]] = {}
    repo_to_group_slugs: dict[str, set[str]] = {}
    warnings: list[str] = []
    ordered_slugs: list[str] = []

    for entry in configured_lists:
        if not isinstance(entry, dict):
            continue

        slug = str(entry.get("slug") or "").strip()
        name = str(entry.get("name") or "").strip()
        if not slug or not name:
            continue

        if slug in groups:
            warnings.append(f"Duplicate list slug '{slug}' in mapping file.")
            continue

        groups[slug] = {
            "slug": slug,
            "name": name,
            "description": str(entry.get("description") or ""),
            "repos": [],
        }
        ordered_slugs.append(slug)

        mapped_repos = entry.get("repos") or []
        if not isinstance(mapped_repos, list):
            continue

        for repo_name in mapped_repos:
            if not isinstance(repo_name, str):
                continue
            normalized_name = repo_name.strip().lower()
            if not normalized_name:
                continue
            if normalized_name not in repo_to_group_slugs:
                repo_to_group_slugs[normalized_name] = set()
            repo_to_group_slugs[normalized_name].add(slug)

    groups[unlisted_slug] = unlisted_group
    ordered_slugs.append(unlisted_slug)

    for repo in starred_repos:
        full_name = str(repo.get("full_name") or "").strip()
        if not full_name:
            continue
        repo_key = full_name.lower()
        assigned_slugs = repo_to_group_slugs.get(repo_key)
        if assigned_slugs:
            for slug in ordered_slugs:
                if slug in assigned_slugs:
                    groups[slug]["repos"].append(repo)
        else:
            groups[unlisted_slug]["repos"].append(repo)

    dataset = {
        "username": username,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_repos": len(starred_repos),
        "groups": [groups[slug] for slug in ordered_slugs if slug in groups],
    }
    return dataset, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch GitHub stars and generate grouped JSON for the website."
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        default=DEFAULT_MAPPING_PATH,
        help=f"Path to starred mapping JSON (default: {DEFAULT_MAPPING_PATH})",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"Path to generated grouped JSON (default: {DEFAULT_OUTPUT_PATH})",
    )
    parser.add_argument(
        "--username",
        type=str,
        default=None,
        help="Override GitHub username defined in mapping file.",
    )
    parser.add_argument(
        "--token-env",
        type=str,
        default="GITHUB_TOKEN",
        help="Environment variable name containing a GitHub token (default: GITHUB_TOKEN).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.mapping.exists():
        print(f"Mapping file not found: {args.mapping}", file=sys.stderr)
        return 1

    mapping = load_json_file(args.mapping)
    if not isinstance(mapping, dict):
        print("Mapping file must be a JSON object.", file=sys.stderr)
        return 1

    if args.username:
        mapping["username"] = args.username

    username = mapping.get("username")
    if not isinstance(username, str) or not username:
        print("GitHub username is missing. Set 'username' in mapping or pass --username.", file=sys.stderr)
        return 1

    token = os.environ.get(args.token_env)
    try:
        starred_repos = fetch_all_starred_repos(username, token)
        dataset, warnings = build_grouped_dataset(mapping, starred_repos)
    except Exception as error:  # noqa: BLE001
        print(f"Failed to sync stars: {error}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(dataset, handle, indent=2)
        handle.write("\n")

    print(f"Fetched {len(starred_repos)} starred repositories for {username}.")
    print(f"Wrote grouped dataset to {args.output}.")

    unlisted_group = next(
        (group for group in dataset["groups"] if group.get("slug") == (mapping.get("unlisted", {}) or {}).get("slug", "to-classify")),
        None,
    )
    if isinstance(unlisted_group, dict):
        unlisted_repos = unlisted_group.get("repos", [])
        if isinstance(unlisted_repos, list) and unlisted_repos:
            print(f"{len(unlisted_repos)} repositories are still unassigned.")

    for warning in warnings:
        print(f"Warning: {warning}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
