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
import anthology_compiler
import character_mastery_engine
import cosmic_ephemeris_engine

def run_simulation(steps=None, target_chapter=None, gut_delta=1, dry_run=False, auto_compile=True):
    """
    Executes sequential round-robin chapters across the galaxy:
    - If target_chapter is given (e.g. 20), simulates until all 74 books reach target_chapter (1,480 total chapters).
    - If steps is given, simulates exactly N steps.
    """
    rot = chapter_engine.read_rotation_tracker()
    curr_b = rot["active_book_index"]
    curr_c = rot["active_chapter_number"]
    curr_gut = rot["current_gut"]

    if target_chapter is not None:
        target_chap = int(target_chapter)
        # Calculate remaining steps to reach Book 74 Chapter target_chap
        total_target_chapters = 74 * target_chap
        current_completed = ((curr_c - 1) * 74) + (curr_b - 1)
        steps = max(0, total_target_chapters - current_completed)
    else:
        steps = int(steps or 1)

    simulated_history = []
    diary_entries = []
    total_words_generated = 0
    readability_scores = []

    print(f"=== INITIATING STELLAR CONFLUENCE UNIVERSE SIMULATION ===")
    print(f"Target Chapters to Generate: {steps} | Current GUT: {curr_gut}")

    for step in range(steps):
        char_info = chapter_engine.get_character_info(curr_b)
        hero = char_info["hero"] if char_info else f"Hero {curr_b}"
        title = char_info["title"] if char_info else f"Book {curr_b}"
        world = char_info["world"] if char_info else "Homeworld"

        # 1. Draft Chapter Prose
        draft_res = story_generator.generate_full_chapter_prose(curr_b, curr_c, save=not dry_run)
        total_words = draft_res.get("total_words", 800)
        total_words_generated += total_words

        # 2. Evaluate Prose Body
        if not dry_run and draft_res.get("saved_to_file"):
            eval_res = chapter_prose_evaluator.evaluate_file(draft_res["saved_to_file"])
        else:
            eval_res = chapter_prose_evaluator.evaluate_prose(draft_res.get("chapter_prose", ""))
        
        fkgl = eval_res.get("flesch_kincaid_grade_level", 5.2)
        readability_scores.append(fkgl)

        synopsis = f"{hero} ({draft_res.get('rank', 'Artisan')}) mastered {draft_res.get('phase', 'trial')} in '{draft_res.get('chapter_title', 'Mission')}', stabilizing the sector Confluence relay."

        # 3. State & Mastery Update
        if not dry_run:
            # Award XP
            character_mastery_engine.award_experience(
                curr_b, 150, f"Completed Book {curr_b} Chapter {curr_c}: {synopsis[:40]}",
                curr_c, curr_gut
            )
            # Log diary entry
            diary_entries.append(f"| GUT {curr_gut} | Book {curr_b:02d} ({title}) | Ch {curr_c:02d} | {hero} | {synopsis} |\n")

        simulated_history.append({
            "step": step + 1,
            "book_id": curr_b,
            "chapter_num": curr_c,
            "gut": curr_gut,
            "hero": hero,
            "title": title,
            "chapter_title": draft_res.get("chapter_title", ""),
            "rank": draft_res.get("rank", ""),
            "total_words": total_words,
            "fkgl": fkgl
        })

        # Advance in-memory rotation
        curr_b += 1
        if curr_b > 74:
            curr_b = 1
            curr_c += 1
        curr_gut += gut_delta

        if (step + 1) % 74 == 0 or (step + 1) == steps:
            print(f" [Progress] Generated {step + 1}/{steps} chapters | Current: Book {curr_b:02d} Ch {curr_c:02d} | GUT: {curr_gut}")

    # 4. Flush State to Disk
    if not dry_run and steps > 0:
        # Write diary
        header_needed = not os.path.exists(chapter_engine.DIARY_MD)
        with open(chapter_engine.DIARY_MD, "a", encoding="utf-8") as f:
            if header_needed:
                f.write("# The Stellar Confluence Universe: Diary of Completed Chapters\n\n")
                f.write("| GUT | Book | Chapter | Character | Synopsis / Action Summary |\n")
                f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            f.writelines(diary_entries)

        # Propagate ephemeris to final GUT
        cosmic_ephemeris_engine.propagate_ephemeris(rot["current_gut"], curr_gut, save=True)

        # Update rotation tracker
        advance_rotation.write_rotation_tracker(curr_b, curr_c, curr_gut)

        # Auto compile manuscripts
        if auto_compile:
            print(" Compiling all 74 full manuscripts...")
            compile_res = anthology_compiler.compile_all_books()
            print(f" Compiled {compile_res.get('total_books_compiled')} manuscripts ({compile_res.get('total_universe_words')} words).")

    avg_fkgl = round(sum(readability_scores) / max(1, len(readability_scores)), 2) if readability_scores else 5.2

    return {
        "simulation_status": "COMPLETED",
        "dry_run": dry_run,
        "total_chapters_simulated": steps,
        "total_steps_executed": steps,
        "total_words_generated": total_words_generated,
        "average_flesch_kincaid_grade_level": avg_fkgl,
        "final_rotation_state": {
            "active_book": curr_b,
            "active_chapter": curr_c,
            "current_gut": curr_gut
        },
        "sample_history": simulated_history[:5] + simulated_history[-5:] if len(simulated_history) > 10 else simulated_history
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Universe Story Simulation Loop")
    parser.add_argument("--steps", type=int, help="Number of sequential chapters to simulate")
    parser.add_argument("--target-chapter", type=int, default=20, help="Target chapter for all 74 books (e.g. 20 for full 1,480 chapters)")
    parser.add_argument("--gut-delta", type=int, default=1, help="GUT ticks to advance per chapter")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing files to disk")
    parser.add_argument("--no-compile", action="store_true", help="Skip manuscript compilation")

    args = parser.parse_args()
    res = run_simulation(
        steps=args.steps,
        target_chapter=None if args.steps else args.target_chapter,
        gut_delta=args.gut_delta,
        dry_run=args.dry_run,
        auto_compile=not args.no_compile
    )
    print(json.dumps(res, indent=2))
