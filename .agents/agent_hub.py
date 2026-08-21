#!/usr/bin/env python3
"""
Master Command Hub & Unified Agent CLI for The Stellar Confluence Universe
Provides a high-performance, single-entry-point dispatcher for all skills:
- cosmos (galactic scale generator, infinite star systems, exotic biomes, xenobiology creatures, cultures, sub-factions)
- confluence-chapter-authoring (authoring, evaluation, storyboards, audio scripts, wave physics, faction matrices, relics, quests)
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

def handle_cosmos(args):
    """Dispatches galactic scale generator commands."""
    import galactic_scale_generator
    if args.action in ["explore", "system"]:
        res = galactic_scale_generator.generate_star_system(args.coords or "[0, 0, 0]", args.name)
    elif args.action == "system-full":
        res = galactic_scale_generator.generate_full_planetary_system(args.coords or "[0, 0, 0]", args.name)
    elif args.action == "creature":
        res = galactic_scale_generator.generate_creature_encounter(args.biome, args.name or "wild")
    elif args.action == "culture":
        res = galactic_scale_generator.generate_cultural_profile(args.faction or args.name or "Universal")
    elif args.action == "anomaly":
        res = galactic_scale_generator.generate_cosmic_anomaly(args.coords or "[0, 0, 0]", args.name)
    elif args.action == "ecosystem":
        res = galactic_scale_generator.generate_xenobiology_ecosystem(args.biome, args.name or "eco")
    elif args.action == "enclave":
        res = galactic_scale_generator.generate_subfaction_enclave(args.faction or "Sun-Forged Hegemony", args.name or "enclave")
    else:
        res = {"error": f"Unknown cosmos action: {args.action}"}
    print(json.dumps(res, indent=2))

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
        res = prose_polisher.polish_prose_text(sample, faction=args.faction or "Sun-Forged")
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
        import chapter_authoring_orchestrator
        res = chapter_authoring_orchestrator.prepare_authoring_brief(args.book_id or 1, args.chapter or 1)
        print(json.dumps(res, indent=2))
    elif args.action == "dual-layer":
        import model_prompt_architect
        ctx = model_prompt_architect.build_model_authoring_context(args.book_id or 1, args.chapter or 1)
        print(json.dumps({"dual_layer_brief": ctx}, indent=2))
    elif args.action == "quest":
        import galactic_adventure_engine
        gut_val = getattr(args, "gut", 100) or 100
        res = galactic_adventure_engine.generate_adventure_quest(args.book_id or 1, gut_val, quest_type=getattr(args, "type", None))
        print(json.dumps(res, indent=2))
    elif args.action == "prompt":
        import model_prompt_architect
        if getattr(args, "json", False):
            ctx = model_prompt_architect.build_model_authoring_context(args.book_id or 1, args.chapter or 1, getattr(args, "gut", None))
            print(json.dumps(ctx, indent=2))
        else:
            prompt_str = model_prompt_architect.generate_model_authoring_prompt(args.book_id or 1, args.chapter or 1, getattr(args, "gut", None))
            print(prompt_str)
    elif args.action == "write":
        import chapter_authoring_orchestrator
        b_id = args.book_id or 1
        c_num = args.chapter or 1
        content = args.text or ""
        if args.file and os.path.exists(args.file):
            with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        res = chapter_authoring_orchestrator.save_authored_chapter(b_id, c_num, content, edition=getattr(args, "edition", None))
        print(json.dumps(res, indent=2))
    elif args.action == "evaluate":
        import chapter_prose_evaluator
        if args.file and os.path.exists(args.file):
            res = chapter_prose_evaluator.evaluate_chapter_file(args.file)
        else:
            sample = args.text or "The golden lens hummed with light. Caelum adjusted his copper goggles calmly."
            res = chapter_prose_evaluator.evaluate_chapter_prose(sample)
        print(json.dumps(res, indent=2))
    elif args.action == "complete":
        import chapter_engine
        res = chapter_engine.complete_chapter_generation(synopsis=args.synopsis or "Chapter Completed", gut_delta=args.gut_delta or 1)
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

def handle_transport(args):
    """Dispatches galactic transport & multi-scale mobility commands."""
    import galactic_transport_engine
    if args.action == "catalog":
        res = {"total_vehicles": len(galactic_transport_engine.get_all_vehicles()), "catalog": galactic_transport_engine.TRANSPORT_TIERS}
    elif args.action == "info":
        res = galactic_transport_engine.get_vehicle_profile(args.vehicle) or {"error": f"Vehicle '{args.vehicle}' not found."}
    elif args.action == "simulate":
        res = galactic_transport_engine.calculate_transit_kinetics(args.vehicle, args.dist or 10.0, args.speed or 1.0, args.cargo or 0.0)
    elif args.action == "faction":
        res = galactic_transport_engine.get_faction_vehicle_preference(args.name or "Sun-Forged Hegemony")
    elif args.action == "trip":
        res = galactic_transport_engine.simulate_multiscale_journey(
            origin_coords=args.coords or "[10, 5, 0]",
            dest_coords=getattr(args, "dest_coords", "[-12, 4, 2]") or "[-12, 4, 2]",
            origin_world=args.origin or "Helios Prime",
            dest_world=args.dest or "Aethelgard Gear-City",
            pilot_name=getattr(args, "pilot", "Caelum") or "Caelum"
        )
    else:
        res = {"error": f"Unknown transport action: {args.action}"}
    print(json.dumps(res, indent=2))

def handle_politics(args):
    """Dispatches galactic politics, governance and treaties commands."""
    import galactic_sociology_politics_engine
    if args.action == "list":
        res = {"total_archetypes": len(galactic_sociology_politics_engine.GOVERNANCE_ARCHETYPES), "archetypes": galactic_sociology_politics_engine.GOVERNANCE_ARCHETYPES}
    elif args.action == "governance":
        res = galactic_sociology_politics_engine.get_governance_model(args.faction or "Sun-Forged Hegemony")
    elif args.action == "treaties":
        res = galactic_sociology_politics_engine.get_diplomatic_treaties(args.faction1 or "Sun-Forged Hegemony", args.faction2 or "Astrolabe Engineers")
    elif args.action == "summit":
        res = galactic_sociology_politics_engine.simulate_diplomatic_summit(
            args.faction1 or "Sun-Forged Hegemony",
            args.faction2 or "Void-Bound Monks",
            args.topic or "Shared Stargate Corridors & Navigational Beacons"
        )
    else:
        res = {"error": f"Unknown politics action: {args.action}"}
    print(json.dumps(res, indent=2))

def handle_sociology(args):
    """Dispatches interstellar sociology and cultural traditions commands."""
    import galactic_sociology_politics_engine
    if args.action == "profile":
        res = galactic_sociology_politics_engine.get_sociological_profile(args.world or "Helios Prime")
    elif args.action == "interaction":
        res = galactic_sociology_politics_engine.generate_civic_interaction(args.faction1 or "Sun-Forged Hegemony", args.faction2 or "Void-Bound Monks", args.type or "HOSPITALITY_MEETING")
    elif args.action == "untuned":
        res = galactic_sociology_politics_engine.get_untuned_sociological_profile(args.world or "Aethel-Prime Frontier")
    else:
        res = {"error": f"Unknown sociology action: {args.action}"}
    print(json.dumps(res, indent=2))

def handle_economy(args):
    """Dispatches galactic trade economy, commodities, and currency conversion commands."""
    import galactic_trade_economy
    ed_flag = getattr(args, "edition", None)
    if args.action == "market":
        res = galactic_trade_economy.get_market_prices(args.category, edition=ed_flag)
    elif args.action == "convert":
        res = galactic_trade_economy.convert_currency(args.amount or 100.0, args.from_curr or "SOL_CREDIT", args.to_curr or "GUILD_SCRIP")
    elif args.action == "dispatch":
        res = galactic_trade_economy.dispatch_convoy(args.origin or "Helios Prime", args.dest or "Aethelgard Gear-City", args.cargo or "Photonic Prism Crystals", args.tonnage or 500, args.gut or 100)
    elif args.action == "fluctuate":
        res = galactic_trade_economy.trigger_market_fluctuation(args.commodity or "Photonic Prism Crystals", args.delta or 10.0, args.reason or "Command hub manual update", edition=ed_flag)
    elif args.action == "stockpile":
        res = galactic_trade_economy.get_planetary_stockpile(args.world or "Helios Prime")
    elif args.action == "route":
        res = galactic_trade_economy.analyze_trade_route(args.origin or "Helios Prime", args.dest or "Aethelgard Gear-City", args.cargo or "Photonic Prism Crystals", args.tonnage or 500)
    elif args.action == "crisis":
        res = galactic_trade_economy.trigger_economic_crisis(
            crisis_type=getattr(args, "crisis_type", "SOLAR_FLARE_EMBARGO") or "SOLAR_FLARE_EMBARGO",
            affected_commodity=getattr(args, "commodity", "Photonic Prism Crystals") or "Photonic Prism Crystals",
            price_delta_pct=getattr(args, "delta", 45.0) or 45.0,
            description=getattr(args, "desc", "Stellar corridor temporary closure") or "Stellar corridor temporary closure",
            current_gut=getattr(args, "gut", 100) or 100,
            edition=ed_flag
        )
    else:
        res = {"error": f"Unknown economy action: {args.action}"}
    print(json.dumps(res, indent=2))

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
        if res.get("matched_vehicles"):
            print(sub_sep)
            print(f" {colorize('MATCHED TRANSPORT VEHICLES & MOBILITY:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}")
            for v in res["matched_vehicles"][:3]:
                print(f"   |-- {colorize(v.get('name', 'Vehicle'), TermColor.BRIGHT_CYAN)} [{v.get('tier_title', 'Craft')}] -> {v.get('propulsion_type')}")
        if res.get("matched_governance"):
            print(sub_sep)
            print(f" {colorize('MATCHED GOVERNANCE & POLITICAL CHARTERS:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}")
            for g in res["matched_governance"][:2]:
                print(f"   |-- {colorize(g.get('name', 'Governance'), TermColor.BRIGHT_MAGENTA)} -> {g.get('legal_charter')[:55]}...")
        if res.get("matched_commodities"):
            print(sub_sep)
            print(f" {colorize('MATCHED COMMODITY MARKET GOODS:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}")
            for cm in res["matched_commodities"][:3]:
                print(f"   |-- {colorize(cm.get('name', 'Good'), TermColor.BRIGHT_GREEN)} [{cm.get('current_price')} Credits/{cm.get('unit')}] -> {cm.get('description')[:45]}...")
        if res.get("matched_anomalies"):
            print(sub_sep)
            print(f" {colorize('MATCHED COSMIC ANOMALIES & WONDERS:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}")
            for an in res["matched_anomalies"][:3]:
                print(f"   |-- {colorize(an.get('name', 'Anomaly'), TermColor.BRIGHT_CYAN)} [{an.get('anomaly_id')}] -> {an.get('scientific_basis')[:45]}...")
        if res.get("matched_culinary"):
            print(sub_sep)
            print(f" {colorize('MATCHED CULINARY TRADITIONS & CIVICS:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}")
            for cul in res["matched_culinary"][:3]:
                print(f"   |-- {colorize(cul.get('name', 'Cuisine'), TermColor.BRIGHT_YELLOW)} [{cul.get('culture_group')}] -> {cul.get('description')[:45]}...")
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
        if res.get("matched_creatures"):
            print(sub_sep)
            print(f" {colorize('MATCHED ALIEN XENOBIOLOGY & CREATURES:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}")
            for c in res["matched_creatures"][:3]:
                print(f"   |-- {colorize(c['species_name'], TermColor.BRIGHT_GREEN)} [{c['size_scale']}] | {c['temperament']}")
        if res["matched_inventory_items"]:
            print(sub_sep)
            print(f" {colorize('MATCHED CHARACTER INVENTORY:', TermColor.BOLD, TermColor.BRIGHT_WHITE)}")
            for itm in res["matched_inventory_items"][:3]:
                itm_obj = itm.get("item", {})
                itm_label = itm_obj.get("name", itm_obj.get("item", str(itm_obj))) if isinstance(itm_obj, dict) else str(itm_obj)
                print(f"   |-- {itm.get('book')}: {itm_label}")
        if res["total_results"] == 0:
            print(colorize("   No matching storylines, vehicles, relics, creatures, or active missions found.", TermColor.DIM))
        print(sep + "\n")

def handle_edition(args):
    """Dispatches edition actions (list, info, new, set, migrate)."""
    import edition_manager
    if args.action == "list":
        editions = edition_manager.list_editions()
        if getattr(args, "json", False):
            print(json.dumps(editions, indent=2))
        else:
            w = 95
            sep = colorize("=" * w, TermColor.BRIGHT_CYAN)
            sub_sep = colorize("-" * w, TermColor.DIM)
            print("\n" + sep)
            print(colorize("   *  THE STELLAR CONFLUENCE UNIVERSE: EDITIONS CATALOG  *", TermColor.BOLD, TermColor.BRIGHT_YELLOW))
            print(sep)
            print(f" {'Edition Folder':<50} | {'Books':<6} | {'Chapters':<10} | {'Total Words':<12}")
            print(sub_sep)
            for ed in editions:
                words_fmt = f"{ed['total_words']:,}"
                print(f" {colorize(ed['edition_dir_name'][:50], TermColor.BRIGHT_WHITE):<50} | {ed['total_books']:<6} | {ed['total_chapters']:<10} | {colorize(words_fmt, TermColor.BRIGHT_GREEN):<12}")
            print(sep + "\n")
    elif args.action == "info":
        active = edition_manager.get_active_edition_dir()
        print(json.dumps({"active_edition_name": os.path.basename(active), "active_edition_path": active}, indent=2))
    elif args.action == "new":
        res = edition_manager.create_new_edition(getattr(args, "name", "Iterative Edition") or "Iterative Edition")
        print(json.dumps(res, indent=2))
    elif args.action == "set":
        res = edition_manager.set_active_edition(args.name)
        print(json.dumps(res, indent=2))
    elif args.action == "migrate":
        res = edition_manager.migrate_existing_root_books_to_edition()
        print(json.dumps(res, indent=2))

def handle_read(args):
    """Renders chapter or manuscript text in the terminal with colored formatting."""
    import glob
    import chapter_engine
    from core.edition_manager import get_book_dir
    book_id = args.book or 1
    char_info = chapter_engine.get_character_info(book_id)
    if not char_info:
        print(colorize(f"Error: Book {book_id} not found in registry.", TermColor.BRIGHT_RED))
        sys.exit(1)
    
    ed_flag = getattr(args, "edition", None)
    book_folder = get_book_dir(book_id, edition=ed_flag, create=False)

    if args.full:
        target_file = os.path.join(book_folder, f"Book_{book_id:02d}_Full_Manuscript.md")
        if not os.path.exists(target_file):
            import anthology_compiler
            anthology_compiler.compile_book_manuscript(book_id, edition=ed_flag)
    else:
        chap_num = args.chapter or 1
        target_file = os.path.join(book_folder, f"Book_{book_id:02d}_Chapter_{chap_num:02d}.md")

    if not os.path.exists(target_file):
        print(colorize(f"Notice: Chapter file {target_file} not yet written.", TermColor.BRIGHT_YELLOW))
        print(colorize(f"To author this chapter, run: python .agents/hub.py author prompt --book-id {book_id} --chapter {args.chapter or 1}", TermColor.BRIGHT_CYAN))
        sys.exit(0)

    with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    w = 80
    sep = colorize("=" * w, TermColor.BRIGHT_CYAN)
    print("\n" + sep)
    print(colorize(f"   *  THE STELLAR CONFLUENCE LIBRARY: BOOK {book_id:02d}  *", TermColor.BOLD, TermColor.BRIGHT_YELLOW))
    print(colorize(f"   *  {char_info['title']} ({char_info['hero']} - {char_info['faction']})  *", TermColor.BRIGHT_WHITE))
    print(sep + "\n")

    # Format markdown lines with color highlights
    for line in content.splitlines():
        if line.startswith("# "):
            print(colorize(line, TermColor.BOLD, TermColor.BRIGHT_YELLOW))
        elif line.startswith("## "):
            print("\n" + colorize(line, TermColor.BOLD, TermColor.BRIGHT_CYAN))
        elif line.startswith("**"):
            print(colorize(line, TermColor.BRIGHT_WHITE))
        elif line.startswith("---"):
            print(colorize("-" * w, TermColor.DIM))
        elif '"' in line:
            parts = line.split('"')
            colored_line = ""
            for idx, p in enumerate(parts):
                if idx % 2 == 1:
                    colored_line += colorize(f'"{p}"', TermColor.BRIGHT_YELLOW)
                else:
                    colored_line += p
            print(colored_line)
        else:
            print(line)
    print("\n" + sep + "\n")

def handle_library(args=None):
    """Displays all 74 books with written chapters, titles, heroes, and file paths."""
    import glob
    import chapter_engine
    from core.edition_manager import get_book_dir, get_active_edition_dir
    w = 95
    sep = colorize("=" * w, TermColor.BRIGHT_CYAN)
    sub_sep = colorize("-" * w, TermColor.DIM)
    
    ed_flag = getattr(args, "edition", None) if args else None
    active_ed = ed_flag or os.path.basename(get_active_edition_dir())

    print("\n" + sep)
    print(colorize(f"   *  THE STELLAR CONFLUENCE UNIVERSE: 74-BOOK MASTER LIBRARY  *", TermColor.BOLD, TermColor.BRIGHT_YELLOW))
    print(colorize(f"   *  Edition: {active_ed}  *", TermColor.BRIGHT_CYAN))
    print(sep)
    print(f" {'ID':<4} | {'Book Title':<34} | {'Protagonist':<22} | {'Chapters':<10} | {'Words':<8}")
    print(sub_sep)

    total_words = 0
    total_chaps = 0

    for b_id in range(1, 75):
        char_info = chapter_engine.get_character_info(b_id)
        if not char_info:
            continue
        book_folder = get_book_dir(b_id, edition=ed_flag, create=False)
        ch_files = glob.glob(os.path.join(book_folder, "Book_*_Chapter_*.md")) if os.path.exists(book_folder) else []
        
        words_count = 0
        for cf in ch_files:
            try:
                with open(cf, "r", encoding="utf-8", errors="ignore") as f:
                    words_count += len(re.findall(r'\b\w+\b', f.read()))
            except Exception:
                pass

        total_words += words_count
        total_chaps += len(ch_files)
        chap_display = f"{len(ch_files)} Ch" if ch_files else "0 Ch"

        print(f" {b_id:02d}   | {char_info['title'][:34]:<34} | {char_info['hero'][:22]:<22} | {colorize(chap_display, TermColor.BRIGHT_GREEN):<10} | {words_count:<8}")

    print(sub_sep)
    print(colorize(f" TOTAL UNIVERSE LIBRARY: 74 Books | {total_chaps} Chapters | {total_words:,} Total Words", TermColor.BOLD, TermColor.BRIGHT_GREEN))
    print(sep + "\n")

def handle_story(args):
    """Dispatches story review and compilation actions."""
    if args.action == "compile-all":
        import anthology_compiler
        res = anthology_compiler.compile_all_books(edition=getattr(args, "edition", None))
        print(json.dumps(res, indent=2))
    elif args.action == "review":
        import glob
        import chapter_engine
        import chapter_prose_evaluator
        from core.edition_manager import get_book_dir
        b_id = args.book or 1
        char_info = chapter_engine.get_character_info(b_id)
        if not char_info:
            print(json.dumps({"error": f"Book {b_id} not found"}, indent=2))
            return
        ed_flag = getattr(args, "edition", None)
        book_folder = get_book_dir(b_id, edition=ed_flag, create=False)
        ch_files = sorted(glob.glob(os.path.join(book_folder, "Book_*_Chapter_*.md"))) if os.path.exists(book_folder) else []
        
        eval_reports = []
        for cf in ch_files:
            ev = chapter_prose_evaluator.evaluate_file(cf)
            eval_reports.append({
                "chapter_file": os.path.basename(cf),
                "fkgl": ev.get("flesch_kincaid_grade_level"),
                "total_words": ev.get("total_words"),
                "dialogue": ev.get("dialogue_percentage"),
                "warmth_score": ev.get("fun_and_warmth_score"),
                "cadence": ev.get("audio_cadence", {}).get("cadence_assessment")
            })
        
        avg_fkgl = round(sum(r["fkgl"] for r in eval_reports if r.get("fkgl")) / max(1, len(eval_reports)), 2) if eval_reports else 5.2
        print(json.dumps({
            "book_id": b_id,
            "title": char_info["title"],
            "hero": char_info["hero"],
            "total_chapters_reviewed": len(eval_reports),
            "average_flesch_kincaid_grade_level": avg_fkgl,
            "target_readability": "Grade 4-6 (Ages 9-12)",
            "status": "PASS" if 3.5 <= avg_fkgl <= 7.0 else "WARNING",
            "chapters": eval_reports
        }, indent=2))
    else:
        print(json.dumps({"error": f"Unknown story action: {args.action}"}, indent=2))

def handle_encyclopedia(args):
    """Dispatches Universal Encyclopedia Network actions."""
    import universal_encyclopedia_network
    ed_flag = getattr(args, "edition", None)
    if args.action == "discover":
        coords = [int(x.strip()) for x in args.coords.strip("[]()").split(",")] if getattr(args, "coords", None) else [15, -8, 42]
        res = universal_encyclopedia_network.register_discovery(
            entity_type=args.type or "species",
            name=args.name or "Photonic Light-Moth",
            hero=args.hero or "Caelum Dawnrunner",
            book_id=getattr(args, "book_id", 1) or 1,
            world=getattr(args, "world", "Helios Prime") or "Helios Prime",
            coords=coords,
            gut=getattr(args, "gut", 100) or 100,
            edition=ed_flag
        )
        print(json.dumps(res, indent=2))
    elif args.action == "list":
        res = universal_encyclopedia_network.list_discoveries(entity_type=getattr(args, "type", None), edition=ed_flag)
        print(json.dumps(res, indent=2))
    elif args.action == "search":
        res = universal_encyclopedia_network.search_encyclopedia(args.query or "", edition=ed_flag)
        print(json.dumps(res, indent=2))
    elif args.action == "sample":
        res = universal_encyclopedia_network.update_sample_custody(
            catalog_id=args.catalog_id,
            status=args.status or "IN_SPECTROMETER",
            findings=args.findings or "Analysis completed in vessel research bay.",
            edition=ed_flag
        )
        print(json.dumps(res, indent=2))
    else:
        print(json.dumps({"error": f"Unknown encyclopedia action: {args.action}"}, indent=2))

def handle_energy(args):
    """Dispatches Cosmic Energy Matrix actions."""
    import cosmic_energy_matrix
    ed_flag = getattr(args, "edition", None)
    if args.action == "catalog":
        res = cosmic_energy_matrix.load_energy_matrix(edition=ed_flag)
        print(json.dumps(res, indent=2))
    elif args.action == "discover":
        coords = [int(x.strip()) for x in args.coords.strip("[]()").split(",")] if getattr(args, "coords", None) else [0, 0, 0]
        res = cosmic_energy_matrix.discover_new_energy(
            name=args.name or "Tachyon Harmonic Rift",
            coords=coords,
            frequency_ghz=getattr(args, "frequency", 144.5) or 144.5,
            description=args.description or "Naturally occurring high-frequency resonance field.",
            discoverer=getattr(args, "discoverer", "Caelum Dawnrunner") or "Caelum Dawnrunner",
            book_id=getattr(args, "book_id", 1) or 1,
            edition=ed_flag
        )
        print(json.dumps(res, indent=2))
    elif args.action == "simulate":
        res = cosmic_energy_matrix.simulate_energy_interaction(
            energy_1=args.energy1 or "CONFLUENCE_WAVEFRONT",
            energy_2=args.energy2 or "CORONAL_PLASMA_FLUX",
            facing_angle=getattr(args, "facing", 45.0) or 45.0
        )
        print(json.dumps(res, indent=2))
    elif args.action == "propagate":
        res = cosmic_energy_matrix.calculate_field_propagation(
            energy_key=getattr(args, "energy", "CONFLUENCE_WAVEFRONT") or "CONFLUENCE_WAVEFRONT",
            distance_units=getattr(args, "dist", 5.0) or 5.0,
            facing_angle=getattr(args, "facing", 30.0) or 30.0,
            source_power_mw=getattr(args, "power", 1000.0) or 1000.0
        )
        print(json.dumps(res, indent=2))
    elif args.action == "efficiency":
        res = cosmic_energy_matrix.calculate_drive_efficiency(
            energy_key=getattr(args, "energy", "CONFLUENCE_WAVEFRONT") or "CONFLUENCE_WAVEFRONT",
            vehicle_id=getattr(args, "vehicle", "CONFLUENCE_WAVE_RIDER") or "CONFLUENCE_WAVE_RIDER",
            thermal_sink_pct=getattr(args, "sink", 30.0) or 30.0,
            facing_angle=getattr(args, "facing", 30.0) or 30.0
        )
        print(json.dumps(res, indent=2))
    else:
        print(json.dumps({"error": f"Unknown energy action: {args.action}"}, indent=2))

def handle_lore(args):
    """Dispatches Deep World Lore and foundational science lookups."""
    from core.edition_manager import get_state_file
    lore_file = get_state_file("universe_lore.md", getattr(args, "edition", None))
    if not os.path.exists(lore_file):
        print(colorize("Notice: universe_lore.md not yet found in edition state.", TermColor.BRIGHT_YELLOW))
        return

    with open(lore_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    topic = getattr(args, "topic", "all") or "all"
    if topic == "all":
        print(content)
    else:
        # Search for section header
        topic_lower = topic.lower()
        sections = content.split("## ")
        matched = False
        for sec in sections[1:]:
            title = sec.splitlines()[0].lower()
            if topic_lower in title:
                print("## " + sec)
                matched = True
                break
        if not matched:
            print(colorize(f"Topic '{topic}' not found in universe_lore.md. Showing full document:\n", TermColor.DIM))
            print(content)

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
    print(f"   2. {colorize('Transport & Mobility:', TermColor.BRIGHT_CYAN)}       python .agents/hub.py transport catalog")
    print(f"   3. {colorize('Politics & Governance:', TermColor.BRIGHT_CYAN)}      python .agents/hub.py politics governance")
    print(f"   4. {colorize('Interstellar Sociology:', TermColor.BRIGHT_CYAN)}     python .agents/hub.py sociology profile --world \"Helios Prime\"")
    print(f"   5. {colorize('Trade Economy & Market:', TermColor.BRIGHT_CYAN)}     python .agents/hub.py economy market")
    print(f"   6. {colorize('Cosmos Sector Exploration:', TermColor.BRIGHT_CYAN)}  python .agents/hub.py cosmos explore --coords \"[125, -42, 88]\"")
    print(f"   7. {colorize('Alien Creature Discovery:', TermColor.BRIGHT_CYAN)}   python .agents/hub.py cosmos creature")
    print(f"   8. {colorize('Inspect Storyline Dossier:', TermColor.BRIGHT_CYAN)}  python .agents/hub.py book {active_b}")
    print(f"   9. {colorize('Global Galactic Search:', TermColor.BRIGHT_CYAN)}    python .agents/hub.py search <term>")
    print(f"  10. {colorize('Full System Health Check:', TermColor.BRIGHT_CYAN)}  python .agents/hub.py doctor")
    print(f"  11. {colorize('Sanity & Regression Suite:', TermColor.BRIGHT_CYAN)} python .agents/hub.py test")
    print(f"  12. {colorize('Document Progress (Now):', TermColor.BRIGHT_CYAN)}  python .agents/hub.py document timestamp")
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
    subparsers.add_parser("test", help="Execute complete 130+ sanity & regression test suite")

    # 4. quickstart
    subparsers.add_parser("quickstart", help="Display interactive quickstart guide and recommended agent actions")

    # 5. book (Dossier)
    p_book = subparsers.add_parser("book", help="Display complete 360-degree storyline dossier card")
    p_book.add_argument("book_id", type=int, help="Book index (1-74)")
    p_book.add_argument("--json", action="store_true", help="Output dossier as JSON")

    # 6. search (Global Search)
    p_search = subparsers.add_parser("search", help="Galactic global search across all 74 storylines, vehicles, politics, economy, relics, creatures & inventory")
    p_search.add_argument("query", help="Search keyword or term")
    p_search.add_argument("--json", action="store_true", help="Output results as JSON")

    # 7. cosmos (Galactic Scale Generator)
    p_cosmos = subparsers.add_parser("cosmos", help="Galactic Scale Engine commands for infinite star systems, biomes, creatures & cultures")
    p_cosmos.add_argument("action", choices=["explore", "system", "system-full", "creature", "culture", "anomaly", "ecosystem", "enclave"], help="Cosmos action")
    p_cosmos.add_argument("--coords", default="[125, -42, 88]", help="3D Sector coordinates")
    p_cosmos.add_argument("--name", help="System or entity name")
    p_cosmos.add_argument("--biome", help="Biome ID filter")
    p_cosmos.add_argument("--faction", help="Faction or entity name for culture")

    # 8. transport (Galactic Mobility)
    p_trans = subparsers.add_parser("transport", help="Galactic Transport & Multi-Scale Mobility Engine")
    p_trans.add_argument("action", choices=["catalog", "info", "simulate", "faction", "trip"], help="Transport action")
    p_trans.add_argument("--vehicle", help="Vehicle ID or name")
    p_trans.add_argument("--dist", type=float, default=10.0, help="Distance units")
    p_trans.add_argument("--speed", type=float, default=1.0, help="Speed multiplier")
    p_trans.add_argument("--cargo", type=float, default=0.0, help="Cargo tonnage")
    p_trans.add_argument("--name", help="Faction name for preference lookup")
    p_trans.add_argument("--origin", help="Origin world name")
    p_trans.add_argument("--dest", help="Destination world name")
    p_trans.add_argument("--coords", default="[10, 5, 0]", help="Origin coordinates")
    p_trans.add_argument("--dest-coords", default="[-12, 4, 2]", help="Destination coordinates")
    p_trans.add_argument("--pilot", default="Caelum", help="Pilot name")

    # 9. politics (Galactic Governance & Treaties)
    p_pol = subparsers.add_parser("politics", help="Interstellar Politics & Governance Engine")
    p_pol.add_argument("action", choices=["list", "governance", "treaties", "summit"], help="Politics action")
    p_pol.add_argument("--faction", help="Faction name for governance model")
    p_pol.add_argument("--faction1", help="Primary faction for treaties or summit")
    p_pol.add_argument("--faction2", help="Secondary faction for treaties or summit")
    p_pol.add_argument("--topic", help="Summit agenda topic")

    # 10. sociology (Sociological Profiles & Traditions)
    p_soc = subparsers.add_parser("sociology", help="Interstellar Sociology & Civilizations Engine")
    p_soc.add_argument("action", choices=["profile", "interaction", "untuned"], help="Sociology action")
    p_soc.add_argument("--world", help="World or faction name")
    p_soc.add_argument("--faction1", help="Host faction")
    p_soc.add_argument("--faction2", help="Guest faction")
    p_soc.add_argument("--type", default="HOSPITALITY_MEETING", help="Interaction type")

    # 11. economy (Trade Economy & Market)
    p_eco = subparsers.add_parser("economy", help="Galactic Trade Economy & Currency Engine")
    p_eco.add_argument("action", choices=["market", "convert", "dispatch", "fluctuate", "stockpile", "route", "crisis"], help="Economy action")
    p_eco.add_argument("--category", help="Commodity category filter")
    p_eco.add_argument("--amount", type=float, default=100.0, help="Currency amount to convert")
    p_eco.add_argument("--from-curr", default="SOL_CREDIT", help="Origin currency")
    p_eco.add_argument("--to-curr", default="GUILD_SCRIP", help="Target currency")
    p_eco.add_argument("--origin", help="Origin world")
    p_eco.add_argument("--dest", help="Destination world")
    p_eco.add_argument("--cargo", help="Cargo commodity")
    p_eco.add_argument("--tonnage", type=int, default=500, help="Cargo tonnage")
    p_eco.add_argument("--commodity", help="Commodity for fluctuation")
    p_eco.add_argument("--delta", type=float, help="Percentage delta for price change")
    p_eco.add_argument("--reason", help="Reason for price change")
    p_eco.add_argument("--world", help="World for stockpile query")
    p_eco.add_argument("--gut", type=int, default=100, help="GUT timestamp")
    p_eco.add_argument("--crisis-type", default="SOLAR_FLARE_EMBARGO", help="Type of economic crisis")
    p_eco.add_argument("--desc", help="Description of crisis or reason")
    p_eco.add_argument("--edition", help="Edition folder name or path")

    # 12. author
    p_author = subparsers.add_parser("author", help="Confluence Chapter Authoring commands")
    p_author.add_argument("action", choices=[
        "cycle", "prepare", "complete", "evaluate", "polish", "storyboard", "audiobook", "compile",
        "simulate", "resonance", "voice", "encounter", "physics", "faction", "diplomacy",
        "relic", "soundscape", "draft", "dual-layer", "quest", "prompt", "write"
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
    p_author.add_argument("--style", help="Plot style filter for draft")
    p_author.add_argument("--type", help="Quest type filter for quest")
    p_author.add_argument("--save", action="store_true", help="Save directly to chapter file in 01_Books_Library")
    p_author.add_argument("--dry-run", action="store_true", help="Dry run simulation or cycle")

    # 13. state
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

    # 14. audit
    p_audit = subparsers.add_parser("audit", help="World Engine Audit commands")
    p_audit.add_argument("action", choices=["test", "continuity", "paradox", "physics", "all"], help="Audit action")
    p_audit.add_argument("--file", help="Chapter markdown file path")

    # 15. document
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

    # 16. flow
    p_flow = subparsers.add_parser("flow", help="Prompt-Response Flow journal commands")
    p_flow.add_argument("action", choices=["log", "active", "summary", "new"], help="Flow action")
    p_flow.add_argument("--prompt", help="Developer prompt text")
    p_flow.add_argument("--response", help="Agent response text")
    p_flow.add_argument("--file", help="Override flow file path")

    # 17. edition (Timestamped Version Folders in 01_Books_Library)
    p_ed = subparsers.add_parser("edition", help="Manage timestamped book editions in 01_Books_Library")
    p_ed.add_argument("action", choices=["list", "info", "new", "set", "migrate", "manifesto"], help="Edition action")
    p_ed.add_argument("--name", default="Iterative Edition", help="Name or description for new edition")

    # 18. encyclopedia (Universal Encyclopedia Network - UEN)
    p_enc = subparsers.add_parser("encyclopedia", help="Universal Encyclopedia Network (UEN) discoveries, scanning, and specimen custody")
    p_enc.add_argument("action", choices=["discover", "scan", "sample", "list", "search", "register"], help="Encyclopedia action")
    p_enc.add_argument("--type", choices=["planet", "biome", "species", "mineral", "anomaly", "energy"], help="Entity type")
    p_enc.add_argument("--name", help="Entity common or scientific name")
    p_enc.add_argument("--hero", help="Discovering character name")
    p_enc.add_argument("--book-id", type=int, default=1, help="Book ID of discoverer")
    p_enc.add_argument("--world", help="World where entity was discovered")
    p_enc.add_argument("--coords", help="Sector 3D coordinates, e.g. '[15, -8, 42]'")
    p_enc.add_argument("--gut", type=int, help="GUT timestamp of discovery")
    p_enc.add_argument("--catalog-id", help="Catalog ID for specimen/scanning update")
    p_enc.add_argument("--status", help="Specimen custody status (COLLECTED, IN_SPECTROMETER, UNDER_CRYO_ANALYSIS, ARCHIVED_IN_ROYAL_VAULT)")
    p_enc.add_argument("--findings", help="Laboratory testing findings")
    p_enc.add_argument("--query", help="Search query")
    p_enc.add_argument("--edition", help="Edition folder name or path")

    # 19. energy (Cosmic Energy Matrix & Dynamic Discovery)
    p_eng = subparsers.add_parser("energy", help="Cosmic Energy Matrix and Dynamic Discovery Engine")
    p_eng.add_argument("action", choices=["catalog", "discover", "simulate", "propagate", "efficiency"], help="Energy action")
    p_eng.add_argument("--name", help="Exotic energy name")
    p_eng.add_argument("--energy", default="CONFLUENCE_WAVEFRONT", help="Target energy force key")
    p_eng.add_argument("--coords", help="Sector 3D coordinates")
    p_eng.add_argument("--frequency", type=float, help="Frequency in GHz")
    p_eng.add_argument("--description", help="Physical description of energy force")
    p_eng.add_argument("--discoverer", help="Discoverer name")
    p_eng.add_argument("--book-id", type=int, default=1, help="Book ID")
    p_eng.add_argument("--energy1", help="Primary energy field for interaction simulation")
    p_eng.add_argument("--energy2", help="Secondary energy field for interaction simulation")
    p_eng.add_argument("--facing", type=float, default=45.0, help="Facing angle for simulation")
    p_eng.add_argument("--dist", type=float, default=5.0, help="Distance units in Light-Years")
    p_eng.add_argument("--power", type=float, default=1000.0, help="Source power in MW")
    p_eng.add_argument("--vehicle", default="CONFLUENCE_WAVE_RIDER", help="Vehicle ID for efficiency")
    p_eng.add_argument("--sink", type=float, default=30.0, help="Thermal sink saturation %")
    p_eng.add_argument("--edition", help="Edition folder name or path")

    # 20. lore (Deep World Lore & Foundational Science)
    p_lore = subparsers.add_parser("lore", help="Inspect deep world lore, foundational geology, bio-engineering, and history")
    p_lore.add_argument("topic", nargs="?", default="all", choices=["all", "wavefront", "geology", "bio-engineering", "orreries", "un-tuned", "energies", "traditions"], help="Lore topic to inspect")
    p_lore.add_argument("--edition", help="Edition folder name or path")

    # 21. read (Terminal Story Reader)
    p_read = subparsers.add_parser("read", help="Read chapters or full book manuscripts with rich terminal formatting")
    p_read.add_argument("--book", type=int, default=1, help="Book ID number (1-74)")
    p_read.add_argument("--chapter", type=int, default=1, help="Chapter number (1-20)")
    p_read.add_argument("--full", action="store_true", help="Read full compiled manuscript")
    p_read.add_argument("--edition", help="Edition folder name or path")

    # 22. library (Master 74-Book Library Directory)
    p_lib = subparsers.add_parser("library", help="Display full 74-book library index with word counts and chapters")
    p_lib.add_argument("--edition", help="Edition folder name or path")

    # 23. story (Multi-Book Story Review & Compilation)
    p_story = subparsers.add_parser("story", help="Multi-Book Story Review & Compilation")
    p_story.add_argument("action", choices=["review", "compile-all"], help="Story action")
    p_story.add_argument("--book", type=int, default=1, help="Book ID for review")
    p_story.add_argument("--edition", help="Edition folder name or path")

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
    elif args.command == "edition":
        handle_edition(args)
    elif args.command == "encyclopedia":
        handle_encyclopedia(args)
    elif args.command == "energy":
        handle_energy(args)
    elif args.command == "lore":
        handle_lore(args)
    elif args.command == "read":
        handle_read(args)
    elif args.command == "library":
        handle_library(args)
    elif args.command == "story":
        handle_story(args)
    elif args.command == "book":
        handle_book(args)
    elif args.command == "search":
        handle_search(args)
    elif args.command == "cosmos":
        handle_cosmos(args)
    elif args.command == "transport":
        handle_transport(args)
    elif args.command == "politics":
        handle_politics(args)
    elif args.command == "sociology":
        handle_sociology(args)
    elif args.command == "economy":
        handle_economy(args)
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
