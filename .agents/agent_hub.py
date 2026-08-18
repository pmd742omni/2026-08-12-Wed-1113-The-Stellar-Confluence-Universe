#!/usr/bin/env python3
"""
Master Command Hub & Unified Agent CLI for The Stellar Confluence Universe
Provides a high-performance, single-entry-point dispatcher for all skills:
- confluence-chapter-authoring (authoring, evaluation, storyboards, audio scripts, wave physics, faction matrices, relics)
- universe-state-manager (ephemeris, transit, trade, tension, mastery, relics, ecology, route pathfinding, mesh graph)
- world-engine-audit (physics, continuity, paradox, regression sanity test, comprehensive doctor)
- document-now (version registry, 100+ Ndebele lexicon, automated progress logs, version registration)
- prompt-response-flow (pair-programming interaction journal logging, session summaries)
"""

import os
import sys
import json
import re
import math
import argparse
import subprocess

# Ensure core and skills are on sys.path
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
CORE_DIR = os.path.join(AGENT_DIR, "core")
if AGENT_DIR not in sys.path:
    sys.path.insert(0, AGENT_DIR)
if CORE_DIR not in sys.path:
    sys.path.insert(0, CORE_DIR)

from core.agent_core import (
    PROJECT_ROOT,
    SKILLS_DIR,
    SYSTEM_STATE_DIR,
    BOOKS_LIB_DIR,
    PROGRESS_DIR,
    TermColor,
    colorize,
    ensure_sys_path,
    generate_terminal_overview,
    get_rotation_state,
    get_all_characters,
    generate_book_dossier,
    format_book_dossier_terminal,
    search_universe
)

ensure_sys_path()

def run_test_suite():
    """Runs the master in-process regression and sanity suite."""
    import agent_self_test
    res = agent_self_test.run_in_process_tests()
    print(json.dumps(res, indent=2))
    return res.get("overall_status") == "ALL_TESTS_PASS"

def run_doctor_diagnostic():
    """Runs comprehensive system diagnostics across state, physics, continuity, paradoxes, and test suite."""
    import audit_universe_state
    import audit_lore_physics
    import multi_book_consistency_auditor
    import agent_self_test

    print(colorize("\n=== EXECUTING STELLAR CONFLUENCE UNIVERSE SYSTEM DOCTOR ===\n", TermColor.BOLD, TermColor.BRIGHT_CYAN))

    # 1. State Audit
    state_res = audit_universe_state.audit_state()
    state_ok = state_res.get("status") == "PASS"
    state_icon = colorize("[PASS]", TermColor.BRIGHT_GREEN) if state_ok else colorize("[FAIL]", TermColor.BRIGHT_RED)
    files_audited = len(state_res.get("system_state_files", {}))
    print(f" [1/4] Universe State Health: {state_icon} ({files_audited} files audited, {state_res.get('character_registry_count', 0)} books in registry)")

    # 2. Physics & Ephemeris Audit
    physics_res = audit_lore_physics.audit_physics()
    physics_ok = physics_res.get("status") == "PASS"
    physics_icon = colorize("[PASS]", TermColor.BRIGHT_GREEN) if physics_ok else colorize("[FAIL]", TermColor.BRIGHT_RED)
    print(f" [2/4] Celestial Physics Laws: {physics_icon} ({physics_res.get('valid_records', 0)} ephemeris entities verified)")

    # 3. Multi-Book Consistency & Paradox Audit
    paradox_res = multi_book_consistency_auditor.audit_multi_book_consistency()
    paradox_ok = paradox_res.get("status") == "PASS"
    paradox_icon = colorize("[PASS]", TermColor.BRIGHT_GREEN) if paradox_ok else colorize("[FAIL]", TermColor.BRIGHT_RED)
    print(f" [3/4] Multi-Book Paradox Audit: {paradox_icon} ({paradox_res.get('total_consistency_checks_passed', 0)} continuity checks)")

    # 4. Master In-Process Test Suite
    test_res = agent_self_test.run_in_process_tests()
    test_ok = test_res.get("overall_status") == "ALL_TESTS_PASS"
    test_icon = colorize("[PASS]", TermColor.BRIGHT_GREEN) if test_ok else colorize("[FAIL]", TermColor.BRIGHT_RED)
    print(f" [4/4] Automated Sanity Suite: {test_icon} ({test_res.get('passed_tests')} in {test_res.get('total_duration_ms', 0):.1f}ms)")

    all_healthy = state_ok and physics_ok and paradox_ok and test_ok
    status_banner = colorize("\n* UNIVERSE ENGINE STATUS: FULLY HEALTHY & OPERATIONAL *\n", TermColor.BOLD, TermColor.BRIGHT_GREEN) if all_healthy else colorize("\n! UNIVERSE ENGINE WARNINGS DETECTED !\n", TermColor.BOLD, TermColor.BRIGHT_RED)
    print(status_banner)

    return {
        "doctor_status": "HEALTHY" if all_healthy else "ISSUES_DETECTED",
        "universe_state_audit": state_res,
        "celestial_physics_audit": physics_res,
        "paradox_audit": paradox_res,
        "test_suite": test_res
    }

def handle_author(args):
    """Dispatches authoring actions."""
    if args.action == "cycle":
        import chapter_engine
        res = chapter_engine.run_full_authoring_cycle(args.book_id, args.chapter, args.synopsis, args.gut_delta, args.dry_run)
        print(json.dumps(res, indent=2))
    elif args.action == "prepare":
        import chapter_engine
        res = chapter_engine.prepare_next_chapter_stub()
        print(json.dumps(res, indent=2))
    elif args.action == "complete":
        if not args.synopsis:
            print(json.dumps({"error": "Argument --synopsis is required for 'complete' action."}, indent=2))
            sys.exit(1)
        import chapter_engine
        res = chapter_engine.complete_chapter_generation(args.synopsis, args.gut_delta)
        print(json.dumps(res, indent=2))
    elif args.action == "evaluate":
        import chapter_prose_evaluator
        if args.file:
            res = chapter_prose_evaluator.evaluate_file(args.file)
        else:
            sample = args.text or "The twin suns climbed into the copper sky, casting long shadows across the dunes."
            res = chapter_prose_evaluator.evaluate_prose(sample)
        print(json.dumps(res, indent=2))
    elif args.action == "polish":
        import prose_polisher
        sample = args.text or "The solar lens hummed with bright energy."
        res = prose_polisher.polish_prose_text(sample)
        print(json.dumps(res, indent=2))
    elif args.action == "storyboard":
        import scene_storyboard_generator
        text = args.text or "Dramatic solar convergence scene"
        res = scene_storyboard_generator.generate_storyboard(text, book_id=args.book_id or 1)
        print(json.dumps(res, indent=2))
    elif args.action == "audiobook":
        import audiobook_director
        text = args.text or 'The star flared. "Hold your shield!" cried Theron.'
        res = audiobook_director.generate_audiobook_script(text, book_id=args.book_id or 1)
        print(json.dumps(res, indent=2))
    elif args.action == "compile":
        import anthology_compiler
        res = anthology_compiler.compile_book_manuscript(args.book_id or 1)
        print(json.dumps(res, indent=2))
    elif args.action == "simulate":
        import universe_simulation_loop
        res = universe_simulation_loop.run_simulation(steps=args.steps or 1, dry_run=args.dry_run)
        print(json.dumps(res, indent=2))
    elif args.action == "resonance":
        import calculate_resonance
        res = calculate_resonance.calculate_resonance(args.facing if args.facing is not None else 0.0, args.faction or "Sun-Forged Hegemony", args.loc or "SURFACE")
        print(json.dumps(res, indent=2))
    elif args.action == "voice":
        import character_voice_profiler
        text = args.text or '"Watch your heat gauge through the primary lens."'
        res = character_voice_profiler.analyze_character_dialogue(text, book_id=args.book_id or 1)
        print(json.dumps(res, indent=2))
    elif args.action == "encounter":
        import cross_encounter_engine
        res = cross_encounter_engine.simulate_cross_encounter(args.book1 or 1, args.book2 or 11, args.medium or "SUBSPACE_COMMS")
        print(json.dumps(res, indent=2))
    elif args.action == "physics":
        import confluence_wave_physics
        coords = args.coords or "[10, 5, 0]"
        gut = args.gut if args.gut is not None else 100.0
        vel = [0.0, args.velocity or 0.0, 0.0]
        res = confluence_wave_physics.calculate_wavefront_state(coords, gut, vel)
        print(json.dumps(res, indent=2))
    elif args.action == "faction":
        import faction_matrix
        f_name = args.faction or "Comet-Riders"
        res = faction_matrix.get_faction_profile(f_name)
        print(json.dumps(res, indent=2))
    elif args.action == "diplomacy":
        import faction_diplomacy_engine
        f1 = args.faction1 or "Sun-Forged Hegemony"
        f2 = args.faction2 or "Void-Bound Monks"
        res = faction_diplomacy_engine.get_diplomatic_relation(f1, f2)
        print(json.dumps(res, indent=2))
    elif args.action == "relic":
        import resonance_artifact_engine
        relic = args.relic or "SOLAR_LENS"
        facing = args.facing if args.facing is not None else 15.0
        res = resonance_artifact_engine.calculate_artifact_performance(relic, facing)
        print(json.dumps(res, indent=2))
    elif args.action == "soundscape":
        import sensory_audio_director
        sample = args.text or "The golden lens hummed with a dazzling beam under the hot sun."
        res = sensory_audio_director.analyze_soundscape(sample)
        print(json.dumps(res, indent=2))
    elif args.action == "draft":
        import story_generator
        res = story_generator.generate_full_chapter_prose(args.book_id or 1, args.chapter or 1)
        print(json.dumps(res, indent=2))
    elif args.action == "quest":
        import galactic_adventure_engine
        gut_val = getattr(args, "gut", 100) or 100
        res = galactic_adventure_engine.generate_adventure_quest(args.book_id or 1, gut_val)
        print(json.dumps(res, indent=2))
    else:
        print(json.dumps({"error": f"Unknown author action: {args.action}"}, indent=2))

def handle_state(args):
    """Dispatches universe state actions."""
    if args.action == "audit":
        import audit_universe_state, audit_lore_physics
        aud = audit_universe_state.audit_state()
        lore = audit_lore_physics.audit_physics()
        print(json.dumps({"universe_state_audit": aud, "lore_physics_audit": lore}, indent=2))
    elif args.action == "dashboard":
        import generate_universe_dashboard
        res = generate_universe_dashboard.generate_dashboard()
        print(json.dumps(res, indent=2))
    elif args.action == "ephemeris":
        import cosmic_ephemeris_engine
        res = cosmic_ephemeris_engine.propagate_ephemeris(args.current_gut or 100, args.target_gut or 101, save=args.save)
        print(json.dumps(res, indent=2))
    elif args.action == "hazards":
        import cosmic_event_bus
        if args.check_sector:
            res = cosmic_event_bus.check_hazards(args.check_sector, args.gut or 100)
        else:
            res = cosmic_event_bus.list_active_events(args.gut or 100)
        print(json.dumps(res, indent=2))
    elif args.action == "tension":
        import galactic_tension_tracker
        f1 = args.faction1 or "Sun-Forged Hegemony"
        f2 = args.faction2 or "Void-Bound Monks"
        if args.delta:
            res = galactic_tension_tracker.adjust_tension(f1, f2, args.delta, args.reason or "Command hub manual update", args.gut or 100)
        else:
            res = galactic_tension_tracker.get_tension(f1, f2)
        print(json.dumps(res, indent=2))
    elif args.action == "trade":
        import galactic_trade_economy
        if args.dispatch:
            res = galactic_trade_economy.dispatch_convoy(args.origin or "Helios Prime", args.destination or "Aethelgard Gear-City", args.commodity or "Photonic Prism Crystals", args.quantity or 100, args.gut or 100)
        else:
            res = galactic_trade_economy.get_market_prices()
        print(json.dumps(res, indent=2))
    elif args.action == "mastery":
        import character_mastery_engine
        if args.award_xp:
            res = character_mastery_engine.award_experience(args.book_id or 1, args.award_xp, args.achievement or "Milestone Completed", args.chapter or 1, args.gut or 100)
        else:
            res = character_mastery_engine.get_character_mastery(args.book_id or 1)
        print(json.dumps(res, indent=2))
    elif args.action == "relics":
        import artifact_ledger_engine
        res = artifact_ledger_engine.list_artifacts()
        print(json.dumps(res, indent=2))
    elif args.action == "ecology":
        import planetary_ecology_matrix
        res = planetary_ecology_matrix.get_planetary_profile(args.world or "Helios Prime")
        print(json.dumps(res, indent=2))
    elif args.action == "relay":
        import subspace_relay_router
        res = subspace_relay_router.route_transmission(args.origin or "[10, 5, 0]", args.target or "[-12, 4, 2]", args.freq or 144.2, ion_storm=args.storm)
        print(json.dumps(res, indent=2))
    elif args.action == "broadcast":
        import galactic_broadcast_feed
        res = galactic_broadcast_feed.get_broadcast_feed()
        print(json.dumps(res, indent=2))
    elif args.action == "transit":
        import interstellar_transit_engine
        if args.start_mission:
            res = interstellar_transit_engine.start_transit_mission(args.book_id or 1, args.origin or "[10, 5, 0]", args.destination or "[16, 5, 0]", args.waypoint_name or "Station Hub", speed=args.speed or 2.0, start_gut=args.gut or 100)
        else:
            res = interstellar_transit_engine.propagate_transits(gut_delta=args.gut_delta or 1)
        print(json.dumps(res, indent=2))
    elif args.action == "route":
        import galactic_navigator
        res = galactic_navigator.plan_interstellar_route(args.origin or "[10, 5, 0]", args.destination or "[-12, 4, 2]")
        print(json.dumps(res, indent=2))
    elif args.action == "mesh":
        import character_mesh_graph
        res = character_mesh_graph.get_character_mesh(args.book_id or 1)
        print(json.dumps(res, indent=2))
    elif args.action == "arcs":
        import character_arc_tracker
        if args.add_item:
            res = character_arc_tracker.add_inventory_item(args.book_id or 1, args.add_item, args.desc or "Acquired item")
        else:
            res = character_arc_tracker.inspect_arc(args.book_id or 1)
        print(json.dumps(res, indent=2))
    elif args.action == "lore":
        import universe_lore_indexer
        res = universe_lore_indexer.get_callbacks_for_book(args.book_id or 1)
        print(json.dumps(res, indent=2))
    elif args.action == "sync":
        import multi_book_sync_engine
        res = multi_book_sync_engine.audit_and_sync_all_books()
        print(json.dumps(res, indent=2))
    elif args.action == "bootstrap":
        import bootstrap_universe_state
        res = bootstrap_universe_state.bootstrap_state()
        print(json.dumps(res, indent=2))
    else:
        print(json.dumps({"error": f"Unknown state action: {args.action}"}, indent=2))

def handle_audit(args):
    """Dispatches audit actions."""
    if args.action == "continuity":
        import chapter_continuity_validator
        res = chapter_continuity_validator.validate_chapter_continuity(args.file or os.path.join(PROJECT_ROOT, "01_Books_Library", "Book_01_The_Solar_Crucible", "Book_01_Chapter_01.md"))
        print(json.dumps(res, indent=2))
    elif args.action == "paradox":
        import multi_book_consistency_auditor
        res = multi_book_consistency_auditor.audit_multi_book_consistency()
        print(json.dumps(res, indent=2))
    elif args.action == "physics":
        import audit_lore_physics
        res = audit_lore_physics.audit_physics()
        print(json.dumps(res, indent=2))
    elif args.action == "test":
        run_test_suite()
    elif args.action == "all":
        run_doctor_diagnostic()
    else:
        print(json.dumps({"error": f"Unknown audit action: {args.action}"}, indent=2))

def handle_document(args):
    """Dispatches document-now actions."""
    import version_registry, get_timestamp
    if args.action == "suggest":
        res = version_registry.suggest_codenames(args.count or 5, category=args.category, search=args.search)
        print(json.dumps(res, indent=2))
    elif args.action == "check":
        if not args.codename:
            print(json.dumps({"error": "Codename required for check"}, indent=2))
            sys.exit(1)
        res = version_registry.check_codename_unique(args.codename)
        print(json.dumps(res, indent=2))
    elif args.action == "next-version":
        res = {"next_version": version_registry.get_next_version()}
        print(json.dumps(res, indent=2))
    elif args.action == "timestamp":
        res = get_timestamp.get_system_timestamps()
        print(json.dumps(res, indent=2))
    elif args.action == "bootstrap":
        res = version_registry.bootstrap_workspace()
        print(json.dumps(res, indent=2))
    elif args.action == "register":
        if not args.version or not args.codename:
            print(json.dumps({"error": "Arguments --version and --codename are required for 'register' action."}, indent=2))
            sys.exit(1)
        res = version_registry.register_version(
            ver_num=args.version,
            codename=args.codename,
            meaning=args.meaning or "Milestone Version",
            date_str=args.date_time or get_timestamp.get_system_timestamps()["human_date_time"],
            filename=args.file or f"progress tracking/{args.version}.md"
        )
        print(json.dumps(res, indent=2))
    else:
        print(json.dumps({"error": f"Unknown document action: {args.action}"}, indent=2))

def handle_flow(args):
    """Dispatches prompt-response flow journal actions."""
    import log_flow_entry
    if args.action == "log":
        if not args.prompt or not args.response:
            print(json.dumps({"error": "--prompt and --response required to log flow entry."}, indent=2))
            sys.exit(1)
        res = log_flow_entry.append_flow_entry(args.prompt, args.response, args.file)
        print(json.dumps(res, indent=2))
    elif args.action == "active":
        active = log_flow_entry.get_active_flow_file()
        print(json.dumps({"active_flow_file": active}, indent=2))
    elif args.action == "summary":
        active = log_flow_entry.get_active_flow_file()
        entry_count = 0
        if active and os.path.exists(active):
            with open(active, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                entry_count = len(re.findall(r"### Prompt", content))
        print(json.dumps({"active_flow_file": active, "total_logged_entries": entry_count}, indent=2))
    elif args.action == "new":
        import datetime
        now = datetime.datetime.now()
        stamp = now.strftime("%Y-%m-%d %a %H%M")
        flow_dir = os.path.join(PROJECT_ROOT, f"{stamp} Prompt-Response Flow")
        os.makedirs(flow_dir, exist_ok=True)
        file_path = os.path.join(flow_dir, f"{stamp} Prompt-Response Flow.md")
        content = f"""---\nName: \"{stamp} Prompt-Response Flow\"\nVersion: \"1.0\"\nDate: \"{stamp}\"\n---\n\n"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(json.dumps({"created_flow_session": file_path}, indent=2))
    else:
        print(json.dumps({"error": f"Unknown flow action: {args.action}"}, indent=2))

def handle_book(args):
    """Dispatches storyline dossier display."""
    if args.json:
        dossier = generate_book_dossier(args.book_id)
        print(json.dumps(dossier, indent=2))
    else:
        print(format_book_dossier_terminal(args.book_id))

def handle_search(args):
    """Dispatches galactic global search."""
    res = search_universe(args.query)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        w = 78
        sep = colorize("=" * w, TermColor.BRIGHT_CYAN)
        sub_sep = colorize("-" * w, TermColor.DIM)
        print("\n" + sep)
        print(colorize(f"   *  GALACTIC SEARCH RESULTS: '{args.query}'  *   ({res['total_results']} Matches Found)", TermColor.BOLD, TermColor.BRIGHT_YELLOW))
        print(sep)
        if res["matched_storylines"]:
            print(f" {colorize('MATCHED STORYLINES & CHARACTERS:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}")
            for b in res["matched_storylines"][:5]:
                print(f"   |-- Book {b['book_id']:02d}: {colorize(b['title'], TermColor.BRIGHT_YELLOW)} | {b['hero']} ({b['faction']}) @ {b['world']}")
        if res["matched_relics"]:
            print(sub_sep)
            print(f" {colorize('MATCHED MASTER RELICS:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}")
            for r in res["matched_relics"][:3]:
                r_type = r.get("relic_type") or r.get("energy_type") or "Master Relic"
                r_cust = r.get("current_custody") or (f"Book {r.get('current_bearer_book')} ({r.get('current_bearer_hero')})" if r.get("current_bearer_book") else "Unknown")
                print(f"   |-- {colorize(r.get('name', 'Relic'), TermColor.BRIGHT_YELLOW)} [{r_type}] in custody of {r_cust}")
        if res["matched_transits"]:
            print(sub_sep)
            print(f" {colorize('MATCHED TRANSIT MISSIONS:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}")
            for t in res["matched_transits"][:3]:
                print(f"   |-- Book {t.get('book_id'):02d} to {t.get('waypoint_name')} (ETA: GUT {t.get('eta_gut')})")
        if res["matched_inventory_items"]:
            print(sub_sep)
            print(f" {colorize('MATCHED CHARACTER INVENTORY:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}")
            for itm in res["matched_inventory_items"][:3]:
                itm_obj = itm.get("item", {})
                itm_label = itm_obj.get("name", itm_obj.get("item", str(itm_obj))) if isinstance(itm_obj, dict) else str(itm_obj)
                print(f"   |-- {itm.get('book')}: {itm_label}")
        if res["total_results"] == 0:
            print(colorize("   No matching storylines, relics, or active missions found.", TermColor.DIM))
        print(sep + "\n")

def handle_quickstart(args=None):
    """Displays an interactive quickstart guide with clear action suggestions."""
    w = 78
    sep = colorize("=" * w, TermColor.BRIGHT_CYAN)
    sub_sep = colorize("-" * w, TermColor.DIM)
    rot = get_rotation_state()
    active_b = rot["active_book_index"]
    active_c = rot["active_chapter_number"]

    print("\n" + sep)
    print(colorize("   *  THE STELLAR CONFLUENCE UNIVERSE: QUICKSTART GUIDE  *", TermColor.BOLD, TermColor.BRIGHT_YELLOW))
    print(sep)
    print(f" Current Active Rotation: {colorize(f'Book {active_b:02d}, Chapter {active_c:02d}', TermColor.BRIGHT_GREEN)}")
    print(sub_sep)
    print(colorize(" RECOMMENDED AGENT WORKFLOWS:", TermColor.BOLD, TermColor.BRIGHT_WHITE))
    print(f"   1. {colorize('One-Shot Chapter Cycle:', TermColor.BRIGHT_CYAN)}   python .agents/hub.py author cycle")
    print(f"   2. {colorize('Inspect Storyline Dossier:', TermColor.BRIGHT_CYAN)}  python .agents/hub.py book {active_b}")
    print(f"   3. {colorize('Global Galactic Search:', TermColor.BRIGHT_CYAN)}    python .agents/hub.py search <term>")
    print(f"   4. {colorize('Full System Health Check:', TermColor.BRIGHT_CYAN)}  python .agents/hub.py doctor")
    print(f"   5. {colorize('Sanity & Regression Suite:', TermColor.BRIGHT_CYAN)} python .agents/hub.py test")
    print(f"   6. {colorize('Document Progress (Now):', TermColor.BRIGHT_CYAN)}  python .agents/hub.py document timestamp")
    print(sep + "\n")

def build_parser():
    parser = argparse.ArgumentParser(
        prog="agent_hub",
        description="Master Command Hub & Unified Agent CLI for The Stellar Confluence Universe"
    )
    subparsers = parser.add_subparsers(dest="command", help="Master Subcommands")

    # 1. overview / status
    subparsers.add_parser("overview", help="Display visual terminal ASCII galactic status board")
    subparsers.add_parser("status", help="Alias for overview")

    # 2. doctor
    subparsers.add_parser("doctor", help="Execute complete system diagnostic health sweep")

    # 3. test
    subparsers.add_parser("test", help="Execute complete 75+ sanity & regression test suite")

    # 4. quickstart
    subparsers.add_parser("quickstart", help="Display interactive quickstart guide and recommended agent actions")

    # 5. book (Dossier)
    p_book = subparsers.add_parser("book", help="Display complete 360-degree storyline dossier card")
    p_book.add_argument("book_id", type=int, help="Book index (1-74)")
    p_book.add_argument("--json", action="store_true", help="Output dossier as JSON")

    # 6. search (Global Search)
    p_search = subparsers.add_parser("search", help="Galactic global search across all 74 storylines, relics, transits & inventory")
    p_search.add_argument("query", help="Search keyword or term")
    p_search.add_argument("--json", action="store_true", help="Output results as JSON")

    # 7. author
    p_author = subparsers.add_parser("author", help="Confluence Chapter Authoring commands")
    p_author.add_argument("action", choices=[
        "cycle", "prepare", "complete", "evaluate", "polish", "storyboard", "audiobook", "compile",
        "simulate", "resonance", "voice", "encounter", "physics", "faction", "diplomacy",
        "relic", "soundscape", "draft", "quest"
    ], help="Authoring action")
    p_author.add_argument("--synopsis", help="Chapter synopsis for 'complete' or 'cycle'")
    p_author.add_argument("--gut-delta", type=int, default=1, help="GUT delta for 'complete' or 'cycle'")
    p_author.add_argument("--gut", type=int, default=100, help="GUT reference timestamp")
    p_author.add_argument("--file", help="File path for evaluation/continuity")
    p_author.add_argument("--text", help="Text payload for analysis/polishing")
    p_author.add_argument("--book-id", type=int, help="Book index (1-74)")
    p_author.add_argument("--chapter", type=int, default=1, help="Chapter number")
    p_author.add_argument("--book1", type=int, help="Book 1 for cross-encounter")
    p_author.add_argument("--book2", type=int, help="Book 2 for cross-encounter")
    p_author.add_argument("--medium", default="SUBSPACE_COMMS", help="Encounter medium")
    p_author.add_argument("--facing", type=float, help="Facing angle degrees")
    p_author.add_argument("--faction", help="Faction name")
    p_author.add_argument("--faction1", help="Primary faction for diplomacy")
    p_author.add_argument("--faction2", help="Secondary faction for diplomacy")
    p_author.add_argument("--relic", help="Relic type for resonance relic engine")
    p_author.add_argument("--coords", help="3D coordinate string, e.g., '[10, 5, 0]'")
    p_author.add_argument("--velocity", type=float, default=0.2, help="Relative velocity fraction of c")
    p_author.add_argument("--freq", type=float, default=144.0, help="Frequency in MHz")
    p_author.add_argument("--loc", help="Location type (SURFACE, ORBITAL, DEEP_SPACE_TRANSIT, GATEWAY_SUBSPACE)")
    p_author.add_argument("--steps", type=int, default=1, help="Simulation steps")
    p_author.add_argument("--dry-run", action="store_true", help="Dry run simulation or cycle")

    # 8. state
    p_state = subparsers.add_parser("state", help="Universe State Manager commands")
    p_state.add_argument("action", choices=[
        "audit", "dashboard", "ephemeris", "hazards", "tension", "trade", "mastery",
        "relics", "ecology", "relay", "broadcast", "transit", "route", "mesh", "arcs", "lore", "sync", "bootstrap"
    ], help="State action")
    p_state.add_argument("--current-gut", type=int, help="Current GUT")
    p_state.add_argument("--target-gut", type=int, help="Target GUT")
    p_state.add_argument("--gut", type=int, help="GUT reference")
    p_state.add_argument("--gut-delta", type=int, default=1, help="GUT delta")
    p_state.add_argument("--save", action="store_true", help="Save ephemeris state")
    p_state.add_argument("--check-sector", help="Sector coordinate string to check hazards")
    p_state.add_argument("--faction1", help="Primary faction")
    p_state.add_argument("--faction2", help="Secondary faction")
    p_state.add_argument("--delta", type=int, help="Tension delta")
    p_state.add_argument("--reason", help="Reason for tension change")
    p_state.add_argument("--dispatch", action="store_true", help="Dispatch trade convoy")
    p_state.add_argument("--origin", help="Origin world/sector")
    p_state.add_argument("--destination", help="Destination world/sector")
    p_state.add_argument("--commodity", help="Trade commodity")
    p_state.add_argument("--quantity", type=int, help="Trade quantity")
    p_state.add_argument("--book-id", type=int, help="Book ID")
    p_state.add_argument("--award-xp", type=int, help="Experience points to award")
    p_state.add_argument("--achievement", help="Achievement description for XP")
    p_state.add_argument("--chapter", type=int, default=1, help="Chapter number")
    p_state.add_argument("--world", help="Planetary world name")
    p_state.add_argument("--target", help="Target sector")
    p_state.add_argument("--freq", type=float, default=144.2, help="Subspace frequency MHz")
    p_state.add_argument("--storm", action="store_true", help="Ion storm interference flag")
    p_state.add_argument("--start-mission", action="store_true", help="Initiate transit mission")
    p_state.add_argument("--waypoint-name", help="Transit destination name")
    p_state.add_argument("--speed", type=float, default=2.0, help="Transit speed")
    p_state.add_argument("--add-item", help="Item name to add to character inventory")
    p_state.add_argument("--desc", help="Item description for character inventory")

    # 9. audit
    p_audit = subparsers.add_parser("audit", help="World Engine Audit commands")
    p_audit.add_argument("action", choices=["test", "continuity", "paradox", "physics", "all"], help="Audit action")
    p_audit.add_argument("--file", help="Chapter markdown file path")

    # 10. document
    p_doc = subparsers.add_parser("document", help="Document-Now workflow commands")
    p_doc.add_argument("action", choices=["bootstrap", "suggest", "check", "next-version", "timestamp", "register"], help="Document action")
    p_doc.add_argument("--codename", help="Proposed Ndebele codename")
    p_doc.add_argument("--category", help="Filter category")
    p_doc.add_argument("--search", help="Search query")
    p_doc.add_argument("--count", type=int, default=5, help="Number of suggestions")
    p_doc.add_argument("--version", help="Version string for register, e.g. 1.9")
    p_doc.add_argument("--meaning", help="Codename meaning for register")
    p_doc.add_argument("--date-time", help="Formatted human date time for register")
    p_doc.add_argument("--file", help="Progress filename for register")

    # 11. flow
    p_flow = subparsers.add_parser("flow", help="Prompt-Response Flow journal commands")
    p_flow.add_argument("action", choices=["log", "active", "summary", "new"], help="Flow action")
    p_flow.add_argument("--prompt", help="Developer prompt text")
    p_flow.add_argument("--response", help="Agent response text")
    p_flow.add_argument("--file", help="Specific flow file path")

    return parser

def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        # Default behavior: Print terminal overview
        print(generate_terminal_overview())
        sys.exit(0)

    if args.command in ["overview", "status"]:
        print(generate_terminal_overview())
    elif args.command == "doctor":
        doc_res = run_doctor_diagnostic()
        sys.exit(0 if doc_res.get("doctor_status") == "HEALTHY" else 1)
    elif args.command == "test":
        success = run_test_suite()
        sys.exit(0 if success else 1)
    elif args.command == "quickstart":
        handle_quickstart(args)
    elif args.command == "book":
        handle_book(args)
    elif args.command == "search":
        handle_search(args)
    elif args.command == "author":
        handle_author(args)
    elif args.command == "state":
        handle_state(args)
    elif args.command == "audit":
        handle_audit(args)
    elif args.command == "document":
        handle_document(args)
    elif args.command == "flow":
        handle_flow(args)

if __name__ == "__main__":
    main()
