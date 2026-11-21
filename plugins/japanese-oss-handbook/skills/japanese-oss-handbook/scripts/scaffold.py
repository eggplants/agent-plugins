#!/usr/bin/env python3
"""Lay out a honkit handbook repository from the japanese-oss-handbook templates.

The templates hold the whole setup of a handbook repository: mise tasks, rumdl,
tombi, actionlint, the CI workflow that deploys to GitHub Pages, Dependabot and
the minimal English README. Existing files are kept unless --force is given.

Example:
  scaffold.py ./acme-cli-handbook --oss-url https://github.com/acme/acme-cli \
      --description "設定ファイルに書いたタスクを実行する acme-cli の使い方"
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "assets" / "template"

# template file -> path in the book repository
FILES = {
    "package.json.tmpl": "package.json",
    "pnpm-workspace.yaml.tmpl": "pnpm-workspace.yaml",
    "book.json.tmpl": "book.json",
    "mise.toml.tmpl": "mise.toml",
    "rumdl.toml.tmpl": ".rumdl.toml",
    "tombi.toml.tmpl": "tombi.toml",
    "gitignore.tmpl": ".gitignore",
    "README.md.tmpl": "README.md",
    "ci.yml.tmpl": ".github/workflows/ci.yml",
    "dependabot.yml.tmpl": ".github/dependabot.yml",
    "website.css.tmpl": "src/styles/website.css",
}

# created only when missing, so that the first build already passes
STUBS = {
    "src/README.md": "# はじめに\n",
    "src/SUMMARY.md": "# Summary\n\n- [はじめに](README.md)\n",
}


def run(cmd: list[str]) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


def detect_owner() -> str:
    return run(["gh", "api", "user", "--jq", ".login"]) or run(["git", "config", "--get", "github.user"])


def slug_of(url: str) -> str:
    path = urlparse(url).path if "://" in url else url
    return path.strip("/").removesuffix(".git")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("book_dir", type=Path, help="the handbook repository to create or fill")
    p.add_argument("--oss-url", required=True, help="URL of the OSS, e.g. https://github.com/acme/acme-cli")
    p.add_argument("--oss-name", help="name shown in the titles (default: the repository name)")
    p.add_argument("--ref-dir", help="directory of the reference clone inside the book (default: the repository name)")
    p.add_argument("--owner", help="GitHub user that will own the handbook repository (default: gh api user)")
    p.add_argument("--repo", help="name of the handbook repository (default: the book directory name)")
    p.add_argument("--title", help='book title (default: "<oss-name> handbook")')
    p.add_argument("--description", default="",
                   help="one Japanese sentence for book.json, e.g. 「〜する acme-cli の使い方」")
    p.add_argument("--force", action="store_true", help="overwrite files that already exist")
    a = p.parse_args()

    book = a.book_dir.expanduser().resolve()
    slug = slug_of(a.oss_url)
    repo_name = slug.rsplit("/", 1)[-1]
    oss_name = a.oss_name or repo_name
    owner = a.owner or detect_owner()
    values = {
        "__OSS_NAME__": oss_name,
        "__OSS_URL__": a.oss_url.removesuffix(".git"),
        "__OSS_SLUG__": slug,
        "__REF_DIR__": a.ref_dir or repo_name,
        "__OWNER__": owner or "__OWNER__",
        "__REPO__": a.repo or book.name,
        "__TITLE__": a.title or f"{oss_name} handbook",
        "__DESCRIPTION__": a.description,
    }

    written, kept = [], []
    for src, dst in FILES.items():
        target = book / dst
        if target.exists() and not a.force:
            kept.append(dst)
            continue
        text = (TEMPLATE_DIR / src).read_text(encoding="utf-8")
        for key, value in values.items():
            text = text.replace(key, value)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        written.append(dst)
    for dst, text in STUBS.items():
        target = book / dst
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
            written.append(dst)
    (book / "src" / "images").mkdir(parents=True, exist_ok=True)

    print(f"book: {book}")
    for dst in written:
        print(f"  wrote {dst}")
    for dst in kept:
        print(f"  kept  {dst} (exists; pass --force to overwrite)")
    problems = []
    if not owner:
        problems.append("GitHub owner unknown: README.md still has __OWNER__ (pass --owner)")
    if not a.description:
        problems.append("book.json has an empty description (pass --description)")
    for msg in problems:
        print(f"WARN {msg}", file=sys.stderr)
    if not shutil.which("mise"):
        print("WARN mise is not on PATH", file=sys.stderr)
    print(
        "next:\n"
        f"  cd {book}\n"
        "  mise trust && mise install\n"
        "  pnpm add -D honkit gitbook-plugin-search-pro   # minimumReleaseAge picks releases 7+ days old\n"
        "  mise run lint && mise run build"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
