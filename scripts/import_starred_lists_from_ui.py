#!/usr/bin/env python3
"""Import GitHub stars lists from the GitHub web UI into local mapping JSON."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote, urlencode, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen


DEFAULT_MAPPING_PATH = Path("data/starred-lists.json")
USER_AGENT = "starred-lists-ui-import/1.0"
GITHUB_ORIGIN = "https://github.com"
BLOCKED_OWNERS = {
    "about",
    "account",
    "apps",
    "blog",
    "collections",
    "contact",
    "customer-stories",
    "docs",
    "enterprise",
    "events",
    "explore",
    "features",
    "github",
    "home",
    "issues",
    "login",
    "logout",
    "marketplace",
    "new",
    "notifications",
    "orgs",
    "organizations",
    "pricing",
    "pulls",
    "search",
    "security",
    "sessions",
    "settings",
    "signup",
    "site",
    "solutions",
    "resources",
    "sponsors",
    "stars",
    "support",
    "team",
    "topics",
    "trending",
    "users",
    "why-github",
}
REPO_PATH_RE = re.compile(r"^/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)$")


class AnchorParser(HTMLParser):
    """Collect anchor href/text/attrs tuples from HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.anchors: list[dict[str, Any]] = []
        self._current_href: str | None = None
        self._current_attrs: dict[str, str] = {}
        self._current_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attrs_dict = {
            key: (value if value is not None else "")
            for key, value in attrs
        }
        href = attrs_dict.get("href")
        if not href:
            return
        self._current_href = href
        self._current_attrs = attrs_dict
        self._current_text = []

    def handle_data(self, data: str) -> None:
        if self._current_href is not None:
            self._current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "a" or self._current_href is None:
            return
        text = " ".join("".join(self._current_text).split())
        self.anchors.append(
            {
                "href": self._current_href,
                "text": text,
                "attrs": self._current_attrs,
            }
        )
        self._current_href = None
        self._current_attrs = {}
        self._current_text = []


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    lowered = re.sub(r"-{2,}", "-", lowered)
    return lowered.strip("-")


def clean_list_name(raw_name: str, fallback: str) -> str:
    name = " ".join(raw_name.split())
    if not name:
        name = fallback.replace("-", " ")
    name = re.sub(r"\s+\d+\s+repositor(?:y|ies)\s*$", "", name, flags=re.IGNORECASE).strip()
    name = re.sub(r"\s*\(?\d+\)?\s*$", "", name).strip()
    return name or fallback.replace("-", " ")


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")


def fetch_html(url: str, cookie: str | None) -> str:
    headers = {
        "Accept": "text/html,application/xhtml+xml",
        "User-Agent": USER_AGENT,
    }
    if cookie:
        headers["Cookie"] = cookie

    request = Request(url, headers=headers)
    with urlopen(request) as response:  # noqa: S310
        return response.read().decode("utf-8", errors="replace")


def parse_anchors(html: str) -> list[dict[str, Any]]:
    parser = AnchorParser()
    parser.feed(html)
    return parser.anchors


def normalize_list_url(username: str, href: str, base_url: str) -> tuple[str | None, str | None]:
    url = urljoin(base_url, href)
    parsed = urlparse(url)
    if parsed.netloc != "github.com":
        return None, None

    query = parse_qs(parsed.query)
    path = parsed.path.rstrip("/")
    list_token: str | None = None
    normalized_path: str
    normalized_query: dict[str, str] = {}

    if path == f"/{username}" and "tab" in query and "stars" in query["tab"]:
        values = query.get("list")
        if values and values[0]:
            list_token = values[0]
            normalized_path = path
            normalized_query = {"tab": "stars", "list": list_token}
        else:
            return None, None
    else:
        match = re.match(rf"^/stars/{re.escape(username)}/lists/([^/]+)$", path)
        if not match:
            return None, None
        list_token = match.group(1)
        normalized_path = path

    if not list_token:
        return None, None

    query_str = urlencode(normalized_query) if normalized_query else ""
    normalized = urlunparse(("https", "github.com", normalized_path, "", query_str, ""))
    return normalized, list_token


def extract_list_links(username: str, stars_page_url: str, anchors: list[dict[str, Any]]) -> list[dict[str, str]]:
    candidates: dict[str, dict[str, str]] = {}
    for anchor in anchors:
        href = str(anchor.get("href") or "").strip()
        if not href:
            continue
        normalized_url, list_token = normalize_list_url(username, href, stars_page_url)
        if not normalized_url or not list_token:
            continue

        fallback_name = list_token.replace("-", " ").replace("_", " ")
        name = clean_list_name(str(anchor.get("text") or ""), fallback_name)
        slug = slugify(list_token) or slugify(name) or "list"

        candidates[normalized_url] = {
            "name": name,
            "slug": slug,
            "url": normalized_url,
        }

    return sorted(candidates.values(), key=lambda item: item["name"].lower())


def extract_repo_full_names(anchors: list[dict[str, Any]], base_url: str) -> set[str]:
    repos: set[str] = set()
    for anchor in anchors:
        href = str(anchor.get("href") or "").strip()
        if not href:
            continue
        url = urljoin(base_url, href)
        parsed = urlparse(url)
        if parsed.netloc != "github.com":
            continue
        if parsed.query or parsed.fragment:
            continue
        match = REPO_PATH_RE.match(parsed.path)
        if not match:
            continue
        owner, repo = match.group(1), match.group(2)
        if owner.lower() in BLOCKED_OWNERS:
            continue
        repos.add(f"{owner}/{repo}")
    return repos


def find_next_page_url(anchors: list[dict[str, Any]], current_url: str) -> str | None:
    for anchor in anchors:
        href = str(anchor.get("href") or "").strip()
        if not href:
            continue
        attrs = anchor.get("attrs") or {}
        rel = str(attrs.get("rel") or "").lower()
        text = str(anchor.get("text") or "").strip().lower()
        is_next = ("next" in rel.split()) or (text == "next")
        if not is_next:
            continue

        next_url = urljoin(current_url, href)
        parsed = urlparse(next_url)
        if parsed.netloc != "github.com":
            continue
        return urlunparse(("https", "github.com", parsed.path, "", parsed.query, ""))
    return None


def fetch_list_repos(list_url: str, cookie: str | None, max_pages: int) -> list[str]:
    repos: set[str] = set()
    current_url: str | None = list_url
    seen_urls: set[str] = set()
    page_count = 0

    while current_url and page_count < max_pages and current_url not in seen_urls:
        seen_urls.add(current_url)
        html = fetch_html(current_url, cookie)
        anchors = parse_anchors(html)
        repos |= extract_repo_full_names(anchors, current_url)
        current_url = find_next_page_url(anchors, current_url)
        page_count += 1

    return sorted(repos, key=lambda item: item.lower())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import GitHub stars list assignments from GitHub web UI."
    )
    parser.add_argument(
        "--mapping",
        type=Path,
        default=DEFAULT_MAPPING_PATH,
        help=f"Path to mapping JSON file (default: {DEFAULT_MAPPING_PATH})",
    )
    parser.add_argument(
        "--username",
        type=str,
        default=None,
        help="Override GitHub username from mapping file.",
    )
    parser.add_argument(
        "--cookie-env",
        type=str,
        default="GITHUB_COOKIE",
        help="Environment variable with GitHub cookie header value (default: GITHUB_COOKIE).",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=25,
        help="Max pagination pages per list (default: 25).",
    )
    parser.add_argument(
        "--preserve-unmatched",
        action="store_true",
        help="Keep local mapping lists that are not present in GitHub UI.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change without writing the mapping file.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.mapping.exists():
        print(f"Mapping file not found: {args.mapping}", file=sys.stderr)
        return 1

    mapping = read_json(args.mapping)
    if not isinstance(mapping, dict):
        print("Mapping file must be a JSON object.", file=sys.stderr)
        return 1

    username = args.username or mapping.get("username")
    if not isinstance(username, str) or not username.strip():
        print("GitHub username is required in mapping file or --username.", file=sys.stderr)
        return 1
    username = username.strip()

    cookie = None
    if args.cookie_env:
        cookie = os.environ.get(args.cookie_env)

    stars_page_url = f"{GITHUB_ORIGIN}/{username}?tab=stars"
    try:
        stars_html = fetch_html(stars_page_url, cookie)
    except HTTPError as error:
        print(f"Failed to fetch stars page: HTTP {error.code}", file=sys.stderr)
        return 1
    except URLError as error:
        print(f"Failed to fetch stars page: {error}", file=sys.stderr)
        return 1

    if "Sign in to GitHub" in stars_html and "/login" in stars_html:
        print(
            "GitHub returned a sign-in page. If your stars are private, set GITHUB_COOKIE and retry.",
            file=sys.stderr,
        )
        return 1

    list_links = extract_list_links(username, stars_page_url, parse_anchors(stars_html))
    if not list_links:
        print(
            "No GitHub star lists found in the stars page UI. Ensure lists exist and are visible.",
            file=sys.stderr,
        )
        return 1

    scraped_lists: list[dict[str, Any]] = []
    failed_lists: list[tuple[str, str]] = []
    for list_info in list_links:
        try:
            repos = fetch_list_repos(list_info["url"], cookie, args.max_pages)
        except HTTPError as error:
            failed_lists.append((list_info["name"], f"HTTP {error.code}"))
            print(
                f"Warning: failed to import list '{list_info['name']}' (HTTP {error.code}).",
                file=sys.stderr,
            )
            continue
        except URLError as error:
            failed_lists.append((list_info["name"], str(error)))
            print(
                f"Warning: failed to import list '{list_info['name']}' ({error}).",
                file=sys.stderr,
            )
            continue

        scraped_lists.append(
            {
                "slug": list_info["slug"],
                "name": list_info["name"],
                "description": "",
                "repos": repos,
            }
        )
        print(f"Imported {len(repos)} repos from list '{list_info['name']}'.")

    if not scraped_lists:
        print("No lists could be imported from GitHub UI.", file=sys.stderr)
        return 1

    existing_lists = mapping.get("lists")
    existing_by_slug: dict[str, dict[str, Any]] = {}
    if isinstance(existing_lists, list):
        for entry in existing_lists:
            if isinstance(entry, dict):
                slug = str(entry.get("slug") or "").strip()
                if slug:
                    existing_by_slug[slug] = entry

    merged_lists: list[dict[str, Any]] = []
    seen_slugs: set[str] = set()
    for entry in scraped_lists:
        slug = str(entry["slug"])
        seen_slugs.add(slug)
        existing = existing_by_slug.get(slug, {})
        description = str(existing.get("description") or "")
        merged_lists.append(
            {
                "slug": slug,
                "name": entry["name"],
                "description": description,
                "repos": entry["repos"],
            }
        )

    if args.preserve_unmatched:
        for slug, existing in existing_by_slug.items():
            if slug in seen_slugs:
                continue
            merged_lists.append(existing)

    mapping["username"] = username
    mapping["lists"] = merged_lists

    if args.dry_run:
        print(f"Dry run complete. Would write {len(merged_lists)} list entries to {args.mapping}.")
        if failed_lists:
            print(f"Skipped {len(failed_lists)} list(s) due fetch errors.", file=sys.stderr)
        return 0

    write_json(args.mapping, mapping)
    print(f"Updated mapping file: {args.mapping}")
    if failed_lists:
        print(f"Skipped {len(failed_lists)} list(s) due fetch errors.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
