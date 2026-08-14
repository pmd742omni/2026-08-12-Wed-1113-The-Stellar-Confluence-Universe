#!/usr/bin/env python3
"""
Confluence Master CLI Dispatcher for The Stellar Confluence Universe
Unified command-line interface orchestrating chapter authoring, prose drafting, universe simulations,
audiobook performance directing, 74-world planetary ecologies, continuity audits, 3D transit vectors,
dual-hero cross encounters, artifact ledgers, wave physics, and 35-point regression diagnostics.
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

    # 1. SIMULATE SUBPARSER (Multi-chapter autonomous loop)
    sim_p = subparsers.add_parser("simulate", help="Run autonomous multi-chapter universe simulation loop")
    sim_p.add_argument("--steps", type=int, default=1, help="Number of sequential chapters to simulate")
    sim_p.add_argument("--gut-delta", type=int, default=1, help="GUT ticks to advance per chapter")
    sim_p.add_argument("--dry-run", action="store_true", help="Simulate without writing files")

    # 2. CHAPTER SUBPARSER
    chap_p = subparsers.add_parser("chapter", help="Chapter authoring, prose drafting, encounter simulation, audio directing & compilation")
    chap_sub = chap_p.add_subparsers(dest="subcommand")

    # chapter prepare
    chap_sub.add_parser("prepare", help="Prepare next round-robin chapter stub & audit constraints")

    # chapter draft
    draft_p = chap_sub.add_parser("draft", help="Autonomous prose drafting co-pilot for high-quality chapter text")
    draft_p.add_argument("--book", type=int, default=1)
    draft_p.add_argument("--chapter", type=int, default=1)
    draft_p.add_argument("--save", action="store_true")

    # chapter audio
    aud_p = chap_sub.add_parser("audio", help="Generate studio-ready audiobook voice acting & sound design script")
    aud_p.add_argument("--file", required=True)
    aud_p.add_argument("--book", type=int, default=1)

    # chapter encounter
    enc_p = chap_sub.add_parser("encounter", help="Simulate dual-hero cross-book dialogue encounter")
    enc_p.add_argument("--book-a", type=int, default=1)
    enc_p.add_argument("--book-b", type=int, default=11)
    enc_p.add_argument("--type", default="SUBSPACE_COMMS")

    # chapter polish
    pol_p = chap_sub.add_parser("polish", help="Polish chapter prose for sensory colors and read-aloud cadence")
    pol_p.add_argument("--file", required=True)
    pol_p.add_argument("--save", action="store_true")

    # chapter compile
    comp_book_p = chap_sub.add_parser("compile", help="Compile individual book chapters into unified publishing manuscript")
    comp_book_p.add_argument("--book", type=int, default=1)

    # chapter complete
    comp_p = chap_sub.add_parser("complete", help="Complete chapter, log diary, propagate ephemeris & advance queue")
    comp_p.add_argument("--synopsis", required=True, help="1-2 sentence synopsis of completed chapter")
    comp_p.add_argument("--gut-delta", type=int, default=1, help="GUT ticks to advance (default: 1)")

    # chapter evaluate
    eval_p = chap_sub.add_parser("evaluate", help="Evaluate chapter prose for 10-year-old child readability & cadence")
    eval_p.add_argument("--file", required=True, help="Path to markdown chapter file")

    # chapter continuity
    cont_p = chap_sub.add_parser("continuity", help="Audit chapter prose against character coordinates & lore continuity")
    cont_p.add_argument("--file", required=True)

    # chapter beats
    beat_p = chap_sub.add_parser("beats", help="Generate 3-act narrative scene beats for current character")
    beat_p.add_argument("--book", type=int, default=1, help="Book ID number (1-74)")

    # 3. UNIVERSE SUBPARSER
    uni_p = subparsers.add_parser("universe", help="Universe state, 74-world ecologies, 3D transit vectors, artifacts, wave physics & dashboard")
    uni_sub = uni_p.add_subparsers(dest="subcommand")

    # universe status
    uni_sub.add_parser("status", help="Display current round-robin queue & universe status")

    # universe dashboard
    uni_sub.add_parser("dashboard", help="Generate interactive HTML/SVG galactic studio dashboard")

    # universe planet
    plan_p = uni_sub.add_parser("planet", help="Query 74-world planetary astrophysics, gravity & resource exports")
    plan_p.add_argument("--world", required=True, help="World name or Book ID number")

    # universe transit
    tr_p = uni_sub.add_parser("transit", help="Manage 3D deep space transit vector flights")
    tr_sub = tr_p.add_subparsers(dest="transit_cmd")
    tr_start = tr_sub.add_parser("start", help="Start deep space transit mission")
    tr_start.add_argument("--book", type=int, required=True)
    tr_start.add_argument("--dest", required=True)
    tr_start.add_argument("--dest-name", default="Target World")
    tr_start.add_argument("--origin", default="[10, 5, 0]")
    tr_start.add_argument("--speed", type=float, default=2.0)
    tr_start.add_argument("--gut", type=int, default=100)
    tr_prop = tr_sub.add_parser("propagate", help="Advance active transit vectors")
    tr_prop.add_argument("--gut-delta", type=int, default=1)
    tr_stat = tr_sub.add_parser("status", help="Get transit progress")
    tr_stat.add_argument("--book", type=int, required=True)

    # universe artifacts
    art_p = uni_sub.add_parser("artifacts", help="Query galactic master relic ledger & lineages")
    art_sub = art_p.add_subparsers(dest="art_cmd")
    art_sub.add_parser("list", help="List all master relics")
    art_ins = art_sub.add_parser("inspect", help="Inspect relic lineage")
    art_ins.add_argument("--name", required=True)
    art_trans = art_sub.add_parser("transfer", help="Transfer relic custody")
    art_trans.add_argument("--name", required=True)
    art_trans.add_argument("--to-book", type=int, required=True)
    art_trans.add_argument("--to-hero", required=True)
    art_trans.add_argument("--gut", type=int, default=100)
    art_trans.add_argument("--reason", required=True)

    # universe broadcast
    bc_p = uni_sub.add_parser("broadcast", help="Query live galactic news wire and subspace radio intercepts")
    bc_p.add_argument("--radio-book", type=int, help="Optional book ID for cockpit radio intercept")

    # universe wave
    wave_p = uni_sub.add_parser("wave", help="Compute 3D Confluence Wavefront wave phase & Doppler shift")
    wave_p.add_argument("--sector", default="[10, 5, 0]")
    wave_p.add_argument("--gut", type=float, default=100.0)
    wave_p.add_argument("--velocity", default="[0, 0, 0]")

    # universe mesh
    mesh_p = uni_sub.add_parser("mesh", help="Inspect character relationship mesh, mentors & comms call-sign")
    mesh_p.add_argument("--book", type=int, default=1)

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

    # 4. FACTION SUBPARSER
    fac_p = subparsers.add_parser("faction", help="Faction physics matrix & diplomacy engine")
    fac_sub = fac_p.add_subparsers(dest="subcommand")

    # faction info
    info_p = fac_sub.add_parser("info", help="Get faction physics, signature equipment & fighting style")
    info_p.add_argument("--name", required=True)

    # faction diplomacy
    dip_p = fac_sub.add_parser("diplomacy", help="Query inter-faction tension, treaties & conflict hooks")
    dip_p.add_argument("--a", required=True)
    dip_p.add_argument("--b", required=True)

    # 5. DOCUMENT SUBPARSER
    doc_p = subparsers.add_parser("document", help="Progress tracking & Ndebele version registry")
    doc_sub = doc_p.add_subparsers(dest="subcommand")

    # document suggest
    sugg_p = doc_sub.add_parser("suggest", help="Suggest Ndebele codenames from 100+ lexicon")
    sugg_p.add_argument("--category", help="Category: Foundation, Cosmos, Energy, Engineering, Movement, Security, Harmony, Wisdom")
    sugg_p.add_argument("--count", type=int, default=5)

    # document check
    chk_p = doc_sub.add_parser("check", help="Check codename uniqueness")
    chk_p.add_argument("--codename", required=True)

    # 6. TEST SUBPARSER
    subparsers.add_parser("test", help="Run automated 35-point agent sanity regression suite")

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
        elif args.subcommand == "audio":
            import audiobook_director
            print(json.dumps(audiobook_director.process_file_to_audio_script(args.file, args.book), indent=2))
        elif args.subcommand == "encounter":
            import cross_encounter_engine
            print(json.dumps(cross_encounter_engine.simulate_cross_encounter(args.book_a, args.book_b, args.type), indent=2))
        elif args.subcommand == "polish":
            import prose_polisher
            print(json.dumps(prose_polisher.polish_chapter_file(args.file, save=args.save), indent=2))
        elif args.subcommand == "compile":
            import anthology_compiler
            print(json.dumps(anthology_compiler.compile_book_manuscript(args.book), indent=2))
        elif args.subcommand == "complete":
            import chapter_engine
            print(json.dumps(chapter_engine.complete_chapter_generation(args.synopsis, args.gut_delta), indent=2))
        elif args.subcommand == "evaluate":
            import chapter_prose_evaluator
            print(json.dumps(chapter_prose_evaluator.evaluate_file(args.file), indent=2))
        elif args.subcommand == "continuity":
            import chapter_continuity_validator
            print(json.dumps(chapter_continuity_validator.validate_chapter_continuity(args.file), indent=2))
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
        elif args.subcommand == "planet":
            import planetary_ecology_matrix
            print(json.dumps(planetary_ecology_matrix.get_planetary_profile(args.world), indent=2))
        elif args.subcommand == "transit":
            import interstellar_transit_engine
            if args.transit_cmd == "start":
                print(json.dumps(interstellar_transit_engine.start_transit_mission(args.book, args.origin, args.dest, args.dest_name, args.speed, args.gut), indent=2))
            elif args.transit_cmd == "propagate":
                print(json.dumps(interstellar_transit_engine.propagate_transits(args.gut_delta), indent=2))
            elif args.transit_cmd == "status":
                print(json.dumps(interstellar_transit_engine.get_transit_status(args.book), indent=2))
            else:
                print(json.dumps(interstellar_transit_engine.propagate_transits(1), indent=2))
        elif args.subcommand == "artifacts":
            import artifact_ledger_engine
            if args.art_cmd == "inspect":
                print(json.dumps(artifact_ledger_engine.inspect_artifact(args.name), indent=2))
            elif args.art_cmd == "transfer":
                print(json.dumps(artifact_ledger_engine.transfer_artifact(args.name, args.to_book, args.to_hero, args.gut, args.reason), indent=2))
            else:
                print(json.dumps(artifact_ledger_engine.list_artifacts(), indent=2))
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
