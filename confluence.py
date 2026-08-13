#!/usr/bin/env python3
"""
Confluence Master CLI Dispatcher for The Stellar Confluence Universe
Unified command-line interface orchestrating chapter authoring, prose drafting, universe simulation loops,
manuscript compilation, celestial ephemerides, wave physics, broadcasts, faction diplomacy, encounters, artifacts, sensory audio, and tests.
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

    # 1. SIMULATE SUBPARSER
    sim_p = subparsers.add_parser("simulate", help="Run autonomous multi-chapter universe simulation loop")
    sim_p.add_argument("--steps", type=int, default=1, help="Number of sequential chapters to simulate")
    sim_p.add_argument("--gut-delta", type=int, default=1, help="GUT ticks to advance per chapter")
    sim_p.add_argument("--dry-run", action="store_true", help="Simulate without writing files")

    # 2. CHAPTER SUBPARSER
    chap_p = subparsers.add_parser("chapter", help="Chapter authoring, prose drafting, compilation & quality evaluation")
    chap_sub = chap_p.add_subparsers(dest="subcommand")

    chap_sub.add_parser("prepare", help="Prepare next round-robin chapter stub & audit constraints")

    draft_p = chap_sub.add_parser("draft", help="Autonomous prose drafting co-pilot for high-quality chapter text")
    draft_p.add_argument("--book", type=int, default=1)
    draft_p.add_argument("--chapter", type=int, default=1)
    draft_p.add_argument("--save", action="store_true")

    comp_book_p = chap_sub.add_parser("compile", help="Compile individual book chapters into unified publishing manuscript")
    comp_book_p.add_argument("--book", type=int, default=1)

    comp_p = chap_sub.add_parser("complete", help="Complete chapter, log diary, propagate ephemeris & advance queue")
    comp_p.add_argument("--synopsis", required=True, help="1-2 sentence synopsis of completed chapter")
    comp_p.add_argument("--gut-delta", type=int, default=1, help="GUT ticks to advance (default: 1)")

    eval_p = chap_sub.add_parser("evaluate", help="Evaluate chapter prose for 10-year-old child readability & cadence")
    eval_p.add_argument("--file", required=True, help="Path to markdown chapter file")

    sensory_p = chap_sub.add_parser("sensory", help="Analyze chapter prose for soundscapes, color palettes & audio cues")
    sensory_p.add_argument("--file", required=True, help="Path to markdown chapter file")

    beat_p = chap_sub.add_parser("beats", help="Generate 3-act narrative scene beats for current character")
    beat_p.add_argument("--book", type=int, default=1, help="Book ID number (1-74)")

    art_p = chap_sub.add_parser("artifact", help="Calculate artifact performance, overheat risk & power consumption")
    art_p.add_argument("--type", default="SOLAR_LENS", help="SOLAR_LENS, VOID_CLOAK, ASTROLABE_FLYWHEEL, GRAVITY_BOARD")
    art_p.add_argument("--angle", type=float, default=15.0, help="Facing angle in degrees (0-180)")

    # 3. UNIVERSE SUBPARSER
    uni_p = subparsers.add_parser("universe", help="Universe state, wave physics, broadcasts, ephemeris & dashboard")
    uni_sub = uni_p.add_subparsers(dest="subcommand")

    uni_sub.add_parser("status", help="Display current round-robin queue & universe status")
    uni_sub.add_parser("dashboard", help="Generate interactive HTML/SVG galactic studio dashboard")

    enc_p = uni_sub.add_parser("encounters", help="Scan for spatial cross-book encounters, proximity & joint engagements")
    enc_p.add_argument("--distance", type=float, default=15.0, help="Max distance threshold in light-AU units")

    bc_p = uni_sub.add_parser("broadcast", help="Query live galactic news wire and subspace radio intercepts")
    bc_p.add_argument("--radio-book", type=int, help="Optional book ID for cockpit radio intercept")

    wave_p = uni_sub.add_parser("wave", help="Compute 3D Confluence Wavefront wave phase & Doppler shift")
    wave_p.add_argument("--sector", default="[10, 5, 0]")
    wave_p.add_argument("--gut", type=float, default=100.0)
    wave_p.add_argument("--velocity", default="[0, 0, 0]")

    mesh_p = uni_sub.add_parser("mesh", help="Inspect character relationship mesh, mentors & comms call-sign")
    mesh_p.add_argument("--book", type=int, default=1)

    eph_p = uni_sub.add_parser("ephemeris", help="Propagate celestial ephemeris across GUT ticks")
    eph_p.add_argument("--advance-by", type=int, default=1)
    eph_p.add_argument("--save", action="store_true")

    route_p = uni_sub.add_parser("route", help="Plan 3D interstellar route & Gateway conduits")
    route_p.add_argument("--origin", required=True)
    route_p.add_argument("--dest", required=True)

    lore_p = uni_sub.add_parser("lore", help="Search universe lore, chapters & callbacks")
    lore_p.add_argument("--search", required=True)

    # 4. FACTION SUBPARSER
    fac_p = subparsers.add_parser("faction", help="Faction physics matrix & diplomacy engine")
    fac_sub = fac_p.add_subparsers(dest="subcommand")

    info_p = fac_sub.add_parser("info", help="Get faction physics, signature equipment & fighting style")
    info_p.add_argument("--name", required=True)

    dip_p = fac_sub.add_parser("diplomacy", help="Query inter-faction tension, treaties & conflict hooks")
    dip_p.add_argument("--a", required=True)
    dip_p.add_argument("--b", required=True)

    # 5. DOCUMENT SUBPARSER
    doc_p = subparsers.add_parser("document", help="Progress tracking & Ndebele version registry")
    doc_sub = doc_p.add_subparsers(dest="subcommand")

    sugg_p = doc_sub.add_parser("suggest", help="Suggest Ndebele codenames from 100+ lexicon")
    sugg_p.add_argument("--category", help="Category: Foundation, Cosmos, Energy, Engineering, Movement, Security, Harmony, Wisdom")
    sugg_p.add_argument("--count", type=int, default=5)

    chk_p = doc_sub.add_parser("check", help="Check codename uniqueness")
    chk_p.add_argument("--codename", required=True)

    # 6. TEST SUBPARSER
    subparsers.add_parser("test", help="Run master automated agent sanity regression suite")

    args = parser.parse_args()

    if args.command == "test":
        sys.exit(run_test_suite())

    elif args.command == "simulate":
        import universe_simulation_loop
        print(json.dumps(universe_simulation_loop.run_simulation(steps=args.steps, gut_delta=args.gut_delta, dry_run=args.dry_run), indent=2))

    elif args.command == "chapter":
        if args.subcommand == "prepare":
            import chapter_engine
            print(json.dumps(chapter_engine.prepare_next_chapter_stub(), indent=2))
        elif args.subcommand == "draft":
            import story_generator
            print(json.dumps(story_generator.generate_full_chapter_prose(args.book, args.chapter, save=args.save), indent=2))
        elif args.subcommand == "compile":
            import anthology_compiler
            print(json.dumps(anthology_compiler.compile_book_manuscript(args.book), indent=2))
        elif args.subcommand == "complete":
            import chapter_engine
            print(json.dumps(chapter_engine.complete_chapter_generation(args.synopsis, args.gut_delta), indent=2))
        elif args.subcommand == "evaluate":
            import chapter_prose_evaluator
            print(json.dumps(chapter_prose_evaluator.evaluate_file(args.file), indent=2))
        elif args.subcommand == "sensory":
            import sensory_audio_director
            with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            print(json.dumps(sensory_audio_director.analyze_soundscape(text), indent=2))
        elif args.subcommand == "artifact":
            import resonance_artifact_engine
            print(json.dumps(resonance_artifact_engine.calculate_artifact_performance(args.type, args.angle), indent=2))
        elif args.subcommand == "beats":
            import chapter_engine, narrative_beat_architect
            char = chapter_engine.get_character_info(args.book)
            if char:
                beats = narrative_beat_architect.generate_scene_beats(
                    char["hero"], char["title"], char["faction"], char["world"], char["loc_type"], 15.0, "PEAK_FACING", "Solar output", "Heat risk"
                )
                print(json.dumps(beats, indent=2))

    elif args.command == "universe":
        if args.subcommand == "status":
            import advance_rotation
            print(json.dumps(advance_rotation.read_rotation_tracker(), indent=2))
        elif args.subcommand == "dashboard":
            import generate_universe_dashboard
            print(json.dumps(generate_universe_dashboard.generate_dashboard(), indent=2))
        elif args.subcommand == "encounters":
            import multi_book_sync_engine
            print(json.dumps(multi_book_sync_engine.detect_encounters(args.distance), indent=2))
        elif args.subcommand == "broadcast":
            import galactic_broadcast_feed
            if args.radio_book:
                print(json.dumps(galactic_broadcast_feed.generate_radio_intercept(args.radio_book), indent=2))
            else:
                print(json.dumps(galactic_broadcast_feed.get_broadcast_feed(), indent=2))
        elif args.subcommand == "wave":
            import confluence_wave_physics
            print(json.dumps(confluence_wave_physics.calculate_wavefront_state(args.sector, args.gut, args.velocity), indent=2))
        elif args.subcommand == "mesh":
            import character_mesh_graph
            print(json.dumps(character_mesh_graph.get_character_mesh(args.book), indent=2))
        elif args.subcommand == "ephemeris":
            import advance_rotation, cosmic_ephemeris_engine
            rot = advance_rotation.read_rotation_tracker()
            curr_g = rot["current_gut"]
            print(json.dumps(cosmic_ephemeris_engine.propagate_ephemeris(curr_g, curr_g + args.advance_by, save=args.save), indent=2))
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
