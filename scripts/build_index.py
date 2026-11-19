"""Builds index.json from the recipes in recipes/.

The CocinaParaLechugones app downloads index.json to search and filter the community
recipe book, then downloads the chosen recipe file. Run by the "Build index" workflow on
every push to main; it can also be run by hand: python scripts/build_index.py

A file that is not a valid `cpl-recipe/1` recipe is reported and left out of the index.
"""

import json
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
RECIPES = ROOT / "recipes"
INDEX = ROOT / "index.json"
FORMAT = "cpl-recipe/1"


def front_matter(text):
    text = text.lstrip("﻿").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise ValueError("no front matter")
    end = text.find("\n---", 4)
    if end < 0:
        raise ValueError("front matter is not closed")
    data = yaml.safe_load(text[4:end])
    if not isinstance(data, dict):
        raise ValueError("front matter is not a mapping")
    return data


def first_added(path):
    """Unix time of the commit that added the file (0 when git has no record of it)."""
    out = subprocess.run(
        ["git", "log", "--diff-filter=A", "--format=%ct", "--", str(path)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    ).stdout.split()
    return int(out[-1]) if out else 0


def entry(path, data):
    if data.get("format") != FORMAT:
        raise ValueError(f"format must be {FORMAT}")
    title = str(data.get("title") or "").strip()
    servings = data.get("servings")
    ingredients = data.get("ingredients")
    if not title or not isinstance(servings, int) or not isinstance(ingredients, list) or not ingredients:
        raise ValueError("title, servings and ingredients are required")
    minutes = [data.get(k) for k in ("prep_minutes", "cook_minutes") if isinstance(data.get(k), int)]
    item = {
        "path": path.relative_to(ROOT).as_posix(),
        "title": title,
        "servings": servings,
    }
    optional = {
        "uid": data.get("uid"),
        "author": data.get("author"),
        "description": data.get("description"),
        "total_minutes": sum(minutes) if minutes else None,
        "tags": sorted({str(t).strip().lower() for t in data.get("tags") or [] if str(t).strip()}),
        "ingredients": [str(i["name"]).strip() for i in ingredients if isinstance(i, dict) and i.get("name")],
    }
    item.update({k: v for k, v in optional.items() if v not in (None, "", [])})
    return item


def main():
    entries, problems = [], []
    for path in sorted(RECIPES.glob("**/*.md")):
        try:
            entries.append((first_added(path), entry(path, front_matter(path.read_text(encoding="utf-8")))))
        except (ValueError, yaml.YAMLError, KeyError, TypeError) as e:
            problems.append(f"{path.relative_to(ROOT).as_posix()}: {e}")
    # Newest first; ties (same commit) by title.
    entries.sort(key=lambda e: (-e[0], e[1]["title"].lower()))
    index = {"format": "cpl-recetario/1", "recipes": [e[1] for e in entries]}
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(entries)} recipes indexed")
    for p in problems:
        print(f"::warning::left out {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
