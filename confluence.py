#!/usr/bin/env python3
"""
Confluence Master CLI Dispatcher for The Stellar Confluence Universe
Unified command-line interface orchestrating chapter authoring, celestial ephemerides,
faction diplomacy, 3D navigation, lore indexing, progress tracking, and regression diagnostics.
"""

import os
import sys
import json
import subprocess
import argparse

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.join(PROJECT_ROOT, ".agents", "skills")

# Add all skills to path
for s in ["document-now", "confluence-chapter-authoring", "universe-state-manager", "prompt-response-flow", "world-engine-audit"]:
    p = os.path.join(SKILLS_DIR, s, "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)

def run_test_suite():
    import agent_self_test
    res = agent_self_test.run_in_process_tests()
    print(json.dumps(res, indent=2))
    return 0 if res["overall_status"] == "ALL_TESTS_PASS" else 1

def main():
    parser = argparse.ArgumentParser(
        prog="confluence",
        description="The Stellar Confluence Universe: Master Command Dispatcher"
    )
    subparsers = parser.add_subparsers(dest="command")

    # 1. CHAPTER SUBPARSER
    chap_p = subparsers.add_parser("chapter", help="Chapter authoring, beat generation & quality evaluation")
    chap_sub = chap_p.add_subparsers(dest="subcommand")

    # chapter prepare
    chap_sub.add_parser("prepare", help="Prepare next round-robin chapter stub & audit constraints")

    # chapter complete
    comp_p = chap_sub.add_parser("complete", help="Complete chapter, log diary, propagate ephemeris & advance queue")
    comp_p.add_argument("--synopsis", required=True, help="1-2 sentence synopsis of completed chapter")
    comp_p.add_argument("--gut-delta", type=int, default=1, help="GUT ticks to advance (default: 1)")

    # chapter evaluate
    eval_p = chap_sub.add_parser("evaluate", help="Evaluate chapter prose for 10-year-old child readability")
    eval_p.add_argument("--file", required=True, help="Path to markdown chapter file")

    # chapter beats
    beat_p = chap_sub.add_parser("beats", help="Generate 3-act narrative scene beats for current character")
    beat_p.add_argument("--book", type=int, default=1, help="Book ID number (1-74)")

    # 2. UNIVERSE SUBPARSER
    uni_p = subparsers.add_parser("universe", help="Universe state, ephemeris, navigation & dashboard")
    uni_sub = uni_p.add_subparsers(dest="subcommand")

    # universe status
    uni_sub.add_parser("status", help="Display current round-robin queue & universe status")

    # universe dashboard
    uni_sub.add_parser("dashboard", help="Generate interactive HTML/SVG galactic radar dashboard")

    # universe ephemeris
    eph_p = uni_sub.add_parser("ephemeris", help="Propagate celestial ephemeris across GUT ticks")
    eph_p.add_argument("--advance-by", type=int, default=1)
    eph_p.add_argument("--save", action="store_true")

    # universe route
    route_p = uni_sub.add_parser("route", help="Plan 3D interstellar route & Gateway conduits")
    route_p.add_argument("--origin", required=True)
    route_p.add_argument("--dest", required=True)

    # universe lore
    lore_p = uni_sub.add_parser("lore", help="Search universe lore, chapters & callbacks")
    lore_p.add_argument("--search", required=True)

    # 3. FACTION SUBPARSER
    fac_p = subparsers.add_parser("faction", help="Faction physics matrix & diplomacy engine")
    fac_sub = fac_p.add_subparsers(dest="subcommand")

    # faction info
    info_p = fac_sub.add_parser("info", help="Get faction physics, signature equipment & fighting style")
    info_p.add_argument("--name", required=True)

    # faction diplomacy
    dip_p = fac_sub.add_parser("diplomacy", help="Query inter-faction tension, treaties & conflict hooks")
    dip_p.add_argument("--a", required=True)
    dip_p.add_argument("--b", required=True)

    # 4. DOCUMENT SUBPARSER
    doc_p = subparsers.add_parser("document", help="Progress tracking & Ndebele version registry")
    doc_sub = doc_p.add_subparsers(dest="subcommand")

    # document suggest
    sugg_p = doc_sub.add_parser("suggest", help="Suggest Ndebele codenames from 100+ lexicon")
    sugg_p.add_argument("--category", help="Category: Foundation, Cosmos, Energy, Engineering, Movement, Security, Harmony, Wisdom")
    sugg_p.add_argument("--count", type=int, default=5)

    # document check
    chk_p = doc_sub.add_parser("check", help="Check codename uniqueness")
    chk_p.add_argument("--codename", required=True)

    # 5. TEST SUBPARSER
    subparsers.add_parser("test", help="Run automated 18-point agent sanity regression suite")

    args = parser.parse_args()

    if args.command == "test":
        sys.exit(run_test_suite())

    elif args.command == "chapter":
        import chapter_engine
        if args.subcommand == "prepare":
            res = chapter_engine.prepare_next_chapter_stub()
            print(json.dumps(res, indent=2))
        elif args.subcommand == "complete":
            res = chapter_engine.complete_chapter_generation(args.synopsis, args.gut_delta)
            print(json.dumps(res, indent=2))
        elif args.subcommand == "evaluate":
            import chapter_prose_evaluator
            res = chapter_prose_evaluator.evaluate_file(args.file)
            print(json.dumps(res, indent=2))
        elif args.subcommand == "beats":
            import narrative_beat_architect
            rot = chapter_engine.read_rotation_tracker()
            char = chapter_engine.get_character_info(args.book)
            if char:
                beats = narrative_beat_architect.generate_scene_beats(
                    char["hero"], char["title"], char["faction"], char["world"], char["loc_type"], 15.0, "PEAK_FACING", "Solar output", "Heat risk"
                )
                print(json.dumps(beats, indent=2))
            else:
                print(json.dumps({"error": f"Book {args.book} not found"}, indent=2))

    elif args.command == "universe":
        if args.subcommand == "status":
            import advance_rotation
            print(json.dumps(advance_rotation.read_rotation_tracker(), indent=2))
        elif args.subcommand == "dashboard":
            import generate_universe_dashboard
            print(json.dumps(generate_universe_dashboard.generate_dashboard(), indent=2))
        elif args.subcommand == "ephemeris":
            import advance_rotation, cosmic_ephemeris_engine
            rot = advance_rotation.read_rotation_tracker()
            curr_g = rot["current_gut"]
            res = cosmic_ephemeris_engine.propagate_ephemeris(curr_g, curr_g + args.advance_by, save=args.save)
            print(json.dumps(res, indent=2))
        elif args.subcommand == "route":
            import galactic_navigator
            print(json.dumps(galactic_navigator.plan_interstellar_route(args.origin, args.dest), indent=2))
        elif args.subcommand == "lore":
            import universe_lore_indexer
            print(json.dumps(universe_lore_indexer.search_lore(args.search), indent=2))

    elif args.command == "faction":
        if args.subcommand == "info":
            import faction_matrix
            print(json.dumps(faction_matrix.get_faction_profile(args.name), indent=2))
        elif args.subcommand == "diplomacy":
            import faction_diplomacy_engine
            print(json.dumps(faction_diplomacy_engine.get_diplomatic_relation(args.a, args.b), indent=2))

    elif args.command == "document":
        import version_registry
        if args.subcommand == "suggest":
            print(json.dumps(version_registry.suggest_codenames(args.count, category=args.category), indent=2))
        elif args.subcommand == "check":
            print(json.dumps(version_registry.check_codename_unique(args.codename), indent=2))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
