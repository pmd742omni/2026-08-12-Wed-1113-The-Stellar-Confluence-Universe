#!/usr/bin/env python3
"""
Galactic Lore, Callback & Cross-Book Memory Indexer for The Stellar Confluence Universe
Indexes authored chapters, character actions, diary entries, and artifacts to provide instant
semantic callbacks and shared universe continuity.
"""

import os
import sys
import json
import glob
import re
import argparse

def find_project_root():
    cwd = os.getcwd()
    curr = cwd
    while True:
        if os.path.exists(os.path.join(curr, "00_System_State")) or os.path.exists(os.path.join(curr, ".git")):
            return curr
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return cwd

PROJECT_ROOT = find_project_root()
SYSTEM_STATE_DIR = os.path.join(PROJECT_ROOT, "00_System_State")
BOOKS_LIB_DIR = os.path.join(PROJECT_ROOT, "01_Books_Library")
DIARY_MD = os.path.join(SYSTEM_STATE_DIR, "diary.md")

def search_lore(query):
    clean_q = query.lower().strip()
    matches = []

    # 1. Search Diary
    if os.path.exists(DIARY_MD):
        with open(DIARY_MD, "r", encoding="utf-8", errors="ignore") as f:
            for idx, line in enumerate(f):
                if clean_q in line.lower() and not line.startswith("#") and ":---" not in line:
                    matches.append({
                        "source": "00_System_State/diary.md",
                        "line_num": idx + 1,
                        "snippet": line.strip()
                    })

    # 2. Search Authored Chapters in 01_Books_Library
    chapter_files = glob.glob(os.path.join(BOOKS_LIB_DIR, "**", "*.md"), recursive=True)
    for cf in chapter_files:
        with open(cf, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        if clean_q in text.lower():
            rel_path = os.path.relpath(cf, PROJECT_ROOT)
            lines = text.split("\n")
            matching_lines = [l.strip() for l in lines if clean_q in l.lower() and len(l.strip()) > 0][:2]
            matches.append({
                "source": rel_path,
                "matches": matching_lines
            })

    return {
        "query": query,
        "total_matches": len(matches),
        "results": matches
    }

def get_callbacks_for_book(book_id):
    """Retrieves relevant nearby characters, historical events, and suggested callbacks."""
    # Read Character Registry to find character info
    char_reg = os.path.join(SYSTEM_STATE_DIR, "character_registry.md")
    hero = f"Hero of Book {int(book_id):02d}"
    world = "Unknown World"
    if os.path.exists(char_reg):
        with open(char_reg, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if f"Book {int(book_id):02d}" in line:
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 6:
                        hero = parts[2].replace("`", "")
                        world = parts[4]
                    break

    # Search for any past mentions of this character in diary or other chapters
    mentions = search_lore(hero)

    # Check recent diary entries
    recent_diary = []
    if os.path.exists(DIARY_MD):
        with open(DIARY_MD, "r", encoding="utf-8", errors="ignore") as f:
            lines = [l.strip() for l in f if l.strip().startswith("|") and "GUT" in l and ":---" not in l]
            recent_diary = lines[-3:] if lines else []

    return {
        "book_id": int(book_id),
        "perspective_character": hero,
        "world": world,
        "cross_book_mentions": mentions["total_matches"],
        "recent_galactic_events": recent_diary,
        "suggested_callbacks": [
            f"Reference the recent celestial communications from neighboring sectors.",
            f"Mention the legend of {hero}'s initial training or first discovery on {world}."
        ]
    }

def get_universe_stats():
    chapter_files = glob.glob(os.path.join(BOOKS_LIB_DIR, "**", "*.md"), recursive=True)
    total_words = 0
    for cf in chapter_files:
        with open(cf, "r", encoding="utf-8", errors="ignore") as f:
            words = re.findall(r'\b\w+\b', f.read())
            total_words += len(words)

    return {
        "total_authored_chapters": len(chapter_files),
        "total_word_count": total_words,
        "total_books_registered": 74
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Galactic Lore & Callback Indexer")
    subparsers = parser.add_subparsers(dest="command")

    # Search
    s_p = subparsers.add_parser("search", help="Search universe lore and chapters")
    s_p.add_argument("--query", required=True)

    # Callbacks
    c_p = subparsers.add_parser("callbacks", help="Get narrative callbacks for a book")
    c_p.add_argument("--book", type=int, required=True)

    # Stats
    subparsers.add_parser("stats", help="Get universe writing stats")

    args = parser.parse_args()

    if args.command == "search":
        print(json.dumps(search_lore(args.query), indent=2))
    elif args.command == "callbacks":
        print(json.dumps(get_callbacks_for_book(args.book), indent=2))
    elif args.command == "stats":
        print(json.dumps(get_universe_stats(), indent=2))
    else:
        print(json.dumps(get_universe_stats(), indent=2))
