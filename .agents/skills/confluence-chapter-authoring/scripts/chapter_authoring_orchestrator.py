#!/usr/bin/env python3
"""
Chapter Authoring Orchestrator for The Stellar Confluence Universe.
Coordinates pure Model-Driven narrative authoring across all 74 storylines,
evaluates dual-audience prose quality (Grade 4-6 readability with mature dramatic stakes),
registers UEN discoveries, and writes chapters directly into the active/target edition.
"""

import os
import sys
import json
import re
import argparse
from typing import Dict, Any, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))))
sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(PROJECT_ROOT, ".agents"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, ".agents", "skills", "universe-state-manager", "scripts"))

from core.edition_manager import get_active_edition_dir, get_book_dir, get_state_file
import model_prompt_architect
import chapter_prose_evaluator
import chapter_engine
import character_mastery_engine
import universal_encyclopedia_network
import cosmic_energy_matrix

def prepare_authoring_brief(book_id: int, chapter_num: int = 1, gut: Optional[int] = None) -> Dict[str, Any]:
    """Generates the structured authoring brief and master prompt for LLM/Subagent authoring."""
    ctx = model_prompt_architect.build_model_authoring_context(book_id, chapter_num, gut)
    prompt_str = model_prompt_architect.generate_model_authoring_prompt(book_id, chapter_num, gut)
    return {
        "book_id": book_id,
        "chapter_num": chapter_num,
        "hero": ctx["hero"],
        "faction": ctx["faction"],
        "context": ctx,
        "model_prompt": prompt_str
    }

def save_authored_chapter(
    book_id: int,
    chapter_num: int,
    chapter_prose: str,
    synopsis: str = "",
    edition: Optional[str] = None
) -> Dict[str, Any]:
    """
    Saves an authored chapter into the target edition directory,
    evaluates its prose quality, and updates edition-scoped state.
    """
    book_dir = get_book_dir(book_id, edition)
    os.makedirs(book_dir, exist_ok=True)
    
    chapter_file = os.path.join(book_dir, f"Book_{book_id:02d}_Chapter_{chapter_num:02d}.md")
    with open(chapter_file, "w", encoding="utf-8") as f:
        f.write(chapter_prose)

    # Run prose evaluation
    eval_result = chapter_prose_evaluator.evaluate_chapter_file(chapter_file)

    # Award character mastery XP
    char_info = chapter_engine.get_character_info(book_id)
    if char_info:
        hero_name = char_info.get("hero", "Hero")
        character_mastery_engine.award_xp(
            hero_name,
            50,
            f"Authored Book {book_id:02d} Chapter {chapter_num:02d}: {eval_result.get('verdict', 'Chapter Completed')}"
        )

    return {
        "status": "CHAPTER_SAVED",
        "book_id": book_id,
        "chapter_num": chapter_num,
        "file_path": chapter_file,
        "edition_directory": os.path.dirname(book_dir),
        "word_count": eval_result.get("word_count", len(re.findall(r'\b\w+\b', chapter_prose))),
        "evaluation": eval_result
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chapter Authoring Orchestrator")
    parser.add_argument("--book-id", type=int, default=1, help="Book ID number (1-74)")
    parser.add_argument("--chapter", type=int, default=1, help="Chapter number (1-20)")
    parser.add_argument("--brief-only", action="store_true", help="Output model authoring prompt")
    parser.add_argument("--edition", help="Target edition folder name or path")

    args = parser.parse_args()
    if args.brief_only:
        brief = prepare_authoring_brief(args.book_id, args.chapter)
        print(brief["model_prompt"])
    else:
        brief = prepare_authoring_brief(args.book_id, args.chapter)
        print(json.dumps(brief["context"], indent=2))
