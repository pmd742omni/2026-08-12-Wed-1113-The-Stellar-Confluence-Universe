#!/usr/bin/env python3
"""
Autonomous Universe Simulation Loop for The Stellar Confluence Universe
Simulates N sequential round-robin chapters across the galaxy: generates prose, audits readability,
logs chapter diaries, propagates 3D celestial ephemerides, and updates the global state engine.
"""

import os
import sys
import json
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

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
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))))

PROJECT_ROOT = find_project_root()
SKILLS_DIR = os.path.join(PROJECT_ROOT, ".agents", "skills")

sys.path.insert(0, SCRIPT_DIR)
sys.path.insert(0, os.path.join(SKILLS_DIR, "universe-state-manager", "scripts"))



import chapter_engine
import story_generator
import chapter_prose_evaluator
import advance_rotation

def run_simulation(steps=1, gut_delta=1, dry_run=False):
    steps = int(steps)
    simulated_history = []

    for step in range(steps):
        rot = chapter_engine.read_rotation_tracker()
        active_b = rot["active_book_index"]
        active_c = rot["active_chapter_number"]
        curr_gut = rot["current_gut"]

        char_info = chapter_engine.get_character_info(active_b)
        hero = char_info["hero"] if char_info else f"Hero {active_b}"
        title = char_info["title"] if char_info else f"Book {active_b}"

        # 1. Draft Chapter Prose
        draft_res = story_generator.generate_full_chapter_prose(active_b, active_c, save=not dry_run)

        # 2. Evaluate Prose
        eval_res = chapter_prose_evaluator.evaluate_prose(draft_res.get("prose_preview", ""))

        synopsis = f"{hero} successfully resolved the active celestial dilemma on {char_info['world'] if char_info else 'their world'}, stabilizing the local Confluence relay."

        # 3. Complete & Advance
        if not dry_run:
            comp_res = chapter_engine.complete_chapter_generation(synopsis, gut_increment=gut_delta)
            next_state = comp_res["next_rotation_state"]
        else:
            next_state = {
                "active_book": (active_b % 74) + 1,
                "active_chapter": active_c + (1 if active_b == 74 else 0),
                "current_gut": curr_gut + gut_delta
            }

        simulated_history.append({
            "step_index": step + 1,
            "book_id": active_b,
            "chapter_num": active_c,
            "gut": curr_gut,
            "hero": hero,
            "title": title,
            "total_words": draft_res["total_words"],
            "readability_grade": eval_res.get("flesch_kincaid_grade_level", 4.5),
            "synopsis": synopsis,
            "next_state": next_state
        })

    return {
        "simulation_status": "COMPLETED",
        "dry_run": dry_run,
        "total_steps_executed": steps,
        "history": simulated_history
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Universe Story Simulation Loop")
    parser.add_argument("--steps", type=int, default=1, help="Number of sequential chapters to simulate")
    parser.add_argument("--gut-delta", type=int, default=1, help="GUT ticks to advance per chapter")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing files to disk")

    args = parser.parse_args()
    res = run_simulation(steps=args.steps, gut_delta=args.gut_delta, dry_run=args.dry_run)
    print(json.dumps(res, indent=2))
