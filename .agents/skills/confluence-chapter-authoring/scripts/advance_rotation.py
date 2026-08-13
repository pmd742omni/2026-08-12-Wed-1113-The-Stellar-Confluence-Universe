#!/usr/bin/env python3
"""
Round-Robin Rotation & State Advancement Engine for The Stellar Confluence Universe
Maintains rotation sequence across all 74 books, tracks chapter increments, and updates 00_System_State files.
"""

import os
import sys
import json
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
ROTATION_TRACKER_MD = os.path.join(SYSTEM_STATE_DIR, "rotation_tracker.md")
DIARY_MD = os.path.join(SYSTEM_STATE_DIR, "diary.md")

def read_rotation_tracker():
    """Reads current book index, chapter number, and GUT from rotation_tracker.md."""
    if not os.path.exists(ROTATION_TRACKER_MD):
        return {
            "active_book_index": 1,
            "active_chapter_number": 1,
            "current_gut": 100,
            "is_fresh": True
        }

    with open(ROTATION_TRACKER_MD, "r", encoding="utf-8") as f:
        content = f.read()

    book_match = re.search(r"Active\s+Book\s+Index\s*:\s*\[?(\d+)\]?", content, re.IGNORECASE)
    chapter_match = re.search(r"Active\s+Chapter\s+Number\s*:\s*\[?(\d+)\]?", content, re.IGNORECASE)
    gut_match = re.search(r"Current\s+Galactic\s+Universal\s+Time\s*\(GUT\)\s*:\s*\[?(\d+)\]?", content, re.IGNORECASE)

    active_book = int(book_match.group(1)) if book_match else 1
    active_chap = int(chapter_match.group(1)) if chapter_match else 1
    curr_gut = int(gut_match.group(1)) if gut_match else 100

    return {
        "active_book_index": active_book,
        "active_chapter_number": active_chap,
        "current_gut": curr_gut,
        "is_fresh": False
    }

def write_rotation_tracker(book_idx, chapter_num, gut):
    """Writes updated rotation tracker markdown file."""
    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    
    # Calculate next queue book
    next_book = (book_idx % 74) + 1
    next_chap = chapter_num + 1 if next_book == 1 else chapter_num

    md_content = f"""# The Stellar Confluence Universe: Rotation Tracker

- **Active Book Index**: {book_idx}
- **Active Chapter Number**: {chapter_num}
- **Current Galactic Universal Time (GUT)**: {gut}
- **Next in Queue**: Book {next_book:02d}, Chapter {next_chap}

## Rotation Loop Architecture
Strict round-robin execution progression across all 74 books:
`[Book 01, Ch {chapter_num}] -> ... -> [Book {book_idx:02d}, Ch {chapter_num}] (ACTIVE) -> ... -> [Book 74, Ch {chapter_num}] -> [Book 01, Ch {chapter_num + 1}]`
"""
    with open(ROTATION_TRACKER_MD, "w", encoding="utf-8") as f:
        f.write(md_content)

def advance_rotation(gut_increment=1, save=True):
    """Computes next book in the round-robin queue and advances state."""
    curr = read_rotation_tracker()
    active_book = curr["active_book_index"]
    active_chap = curr["active_chapter_number"]
    curr_gut = curr["current_gut"]

    next_book = (active_book % 74) + 1
    next_chap = active_chap + 1 if next_book == 1 else active_chap
    next_gut = curr_gut + gut_increment

    if save:
        write_rotation_tracker(next_book, next_chap, next_gut)

    return {
        "previous_state": curr,
        "new_state": {
            "active_book_index": next_book,
            "active_chapter_number": next_chap,
            "current_gut": next_gut
        },
        "saved": save
    }

def append_diary_entry(book_idx, book_title, chapter_num, character_name, gut, summary):
    """Appends an execution log entry to 00_System_State/diary.md."""
    os.makedirs(SYSTEM_STATE_DIR, exist_ok=True)
    header_needed = not os.path.exists(DIARY_MD)

    entry = f"| GUT {gut} | Book {book_idx:02d} ({book_title}) | Ch {chapter_num} | {character_name} | {summary} |\n"

    with open(DIARY_MD, "a", encoding="utf-8") as f:
        if header_needed:
            f.write("# The Stellar Confluence Universe: Diary of Completed Chapters\n\n")
            f.write("| GUT | Book | Chapter | Character | Synopsis / Action Summary |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        f.write(entry)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advance Round-Robin Rotation Tracker")
    parser.add_argument("--status", action="store_true", help="Display current active rotation status")
    parser.add_argument("--advance", action="store_true", help="Advance active rotation to next book in queue")
    parser.add_argument("--gut-delta", type=int, default=1, help="GUT time increment (default: 1)")
    parser.add_argument("--no-save", action="store_true", help="Preview advancement without writing file")
    parser.add_argument("--set-book", type=int, help="Manually set active book index (1-74)")
    parser.add_argument("--set-chapter", type=int, help="Manually set active chapter number")
    parser.add_argument("--set-gut", type=int, help="Manually set current GUT")
    
    args = parser.parse_args()

    if args.set_book is not None or args.set_chapter is not None or args.set_gut is not None:
        curr = read_rotation_tracker()
        b = args.set_book if args.set_book is not None else curr["active_book_index"]
        c = args.set_chapter if args.set_chapter is not None else curr["active_chapter_number"]
        g = args.set_gut if args.set_gut is not None else curr["current_gut"]
        write_rotation_tracker(b, c, g)
        print(json.dumps({"status": "updated", "book": b, "chapter": c, "gut": g}, indent=2))
        sys.exit(0)

    if args.advance:
        res = advance_rotation(gut_increment=args.gut_delta, save=not args.no_save)
        print(json.dumps(res, indent=2))
    else:
        status = read_rotation_tracker()
        print(json.dumps(status, indent=2))
