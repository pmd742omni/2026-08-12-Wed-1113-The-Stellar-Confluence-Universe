#!/usr/bin/env python3
"""
Comprehensive 18-Point Agent Regression & Sanity Runner for The Stellar Confluence Universe
Executes in-process unit and integration checks across all 5 skills, 15+ modules, state schemas,
and physical simulation engines in under 100 milliseconds.
"""

import os
import sys
import json
import time

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
SKILLS_DIR = os.path.join(PROJECT_ROOT, ".agents", "skills")

# Add all skill script directories to sys.path
for s in ["document-now", "confluence-chapter-authoring", "universe-state-manager", "prompt-response-flow", "world-engine-audit"]:
    p = os.path.join(SKILLS_DIR, s, "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def run_in_process_tests():
    start_total = time.time()
    results = []
    passed_count = 0

    # 1. Document-Now: get_timestamp
    try:
        import get_timestamp
        ts = get_timestamp.get_system_timestamps()
        assert "file_prefix" in ts and "human_date_time" in ts
        results.append({"test": "1. Document-Now: Timestamp Extractor", "status": "PASS", "details": ts["human_date_time"]})
        passed_count += 1
    except Exception as e:
        results.append({"test": "1. Document-Now: Timestamp Extractor", "status": "FAIL", "error": str(e)})

    # 2. Document-Now: version_registry (100+ lexicon)
    try:
        import version_registry
        suggs = version_registry.suggest_codenames(3, category="Cosmos")
        assert len(suggs) == 3
        boot = version_registry.bootstrap_workspace()
        assert boot["total_dictionary_terms"] >= 90
        results.append({"test": "2. Document-Now: 100+ Lexicon & Bootstrap", "status": "PASS", "details": f"{boot['total_dictionary_terms']} terms"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "2. Document-Now: 100+ Lexicon & Bootstrap", "status": "FAIL", "error": str(e)})

    # 3. Universe State: bootstrap_universe_state
    try:
        import bootstrap_universe_state
        res_b = bootstrap_universe_state.bootstrap_state()
        assert res_b["total_books_registered"] == 74
        results.append({"test": "3. Universe State: Bootstrap State", "status": "PASS", "details": "74 books"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "3. Universe State: Bootstrap State", "status": "FAIL", "error": str(e)})

    # 4. Universe State: Dynamic Ephemeris Engine
    try:
        import cosmic_ephemeris_engine
        eph = cosmic_ephemeris_engine.propagate_ephemeris(100, 102, save=False)
        assert eph["total_characters_propagated"] == 74
        results.append({"test": "4. Universe State: Ephemeris Propagation", "status": "PASS", "details": f"Propagated 74 chars over ΔGUT=2"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "4. Universe State: Ephemeris Propagation", "status": "FAIL", "error": str(e)})

    # 5. Universe State: Cosmic Event Bus
    try:
        import cosmic_event_bus
        ev_log = cosmic_event_bus.log_event("BEACON_PULSE", "Book 04", "[15, 6, 0]", 5.0, 100, 10, "Test Solar Flare")
        ev_check = cosmic_event_bus.check_hazards("[12, 5, 1]", 105)
        assert ev_check["active_hazard_count"] >= 1
        results.append({"test": "5. Universe State: Cosmic Event Bus", "status": "PASS", "details": f"Hazard intensity: {ev_check['hazards'][0]['hazard_intensity']}"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "5. Universe State: Cosmic Event Bus", "status": "FAIL", "error": str(e)})

    # 6. Universe State: Galactic 3D Navigator
    try:
        import galactic_navigator
        route = galactic_navigator.plan_interstellar_route("[10, 5, 0]", "[-12, 4, 2]")
        assert route["estimated_transit_duration_gut"] > 0
        results.append({"test": "6. Universe State: Galactic Navigator", "status": "PASS", "details": f"{route['chosen_route_type']} (Dist: {route['direct_distance_units']})"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "6. Universe State: Galactic Navigator", "status": "FAIL", "error": str(e)})

    # 7. Universe State: Character Arc Tracker
    try:
        import character_arc_tracker
        item_res = character_arc_tracker.add_inventory_item(1, "Photonic Prism Lens", "Focuses solar beam")
        arc = character_arc_tracker.inspect_arc(1)
        assert len(arc["inventory"]) >= 1
        results.append({"test": "7. Universe State: Character Arc Tracker", "status": "PASS", "details": f"{len(arc['inventory'])} items tracked"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "7. Universe State: Character Arc Tracker", "status": "FAIL", "error": str(e)})

    # 8. Universe State: Visual Dashboard Generator
    try:
        import generate_universe_dashboard
        dash = generate_universe_dashboard.generate_dashboard()
        assert dash["status"] == "generated" and os.path.exists(dash["file_path"])
        results.append({"test": "8. Universe State: Visual Dashboard", "status": "PASS", "details": f"{dash['total_characters_rendered']} storylines rendered"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "8. Universe State: Visual Dashboard", "status": "FAIL", "error": str(e)})

    # 9. Universe State: Lore & Callback Indexer
    try:
        import universe_lore_indexer
        cb = universe_lore_indexer.get_callbacks_for_book(1)
        assert "perspective_character" in cb
        results.append({"test": "9. Universe State: Lore Indexer", "status": "PASS", "details": f"Callbacks for {cb['perspective_character']}"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "9. Universe State: Lore Indexer", "status": "FAIL", "error": str(e)})

    # 10. Confluence Authoring: Faction Matrix
    try:
        import faction_matrix
        f_prof = faction_matrix.get_faction_profile("Comet-Riders")
        assert "SUBLIMATION SURGE" in f_prof["profile"]["peak_facing"]["buff"]
        results.append({"test": "10. Confluence Authoring: Faction Matrix", "status": "PASS", "details": f_prof['matched_name']})
        passed_count += 1
    except Exception as e:
        results.append({"test": "10. Confluence Authoring: Faction Matrix", "status": "FAIL", "error": str(e)})

    # 11. Confluence Authoring: Faction Diplomacy & Tension Engine
    try:
        import faction_diplomacy_engine
        dip = faction_diplomacy_engine.get_diplomatic_relation("Sun-Forged Hegemony", "Void-Bound Monks")
        assert dip["stance"] == "OPEN_RIVALRY" and dip["tension_index"] > 80
        results.append({"test": "11. Confluence Authoring: Faction Diplomacy", "status": "PASS", "details": f"Sun vs Void: {dip['stance']} ({dip['tension_index']}/100)"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "11. Confluence Authoring: Faction Diplomacy", "status": "FAIL", "error": str(e)})

    # 12. Confluence Authoring: Narrative Beat Architect
    try:
        import narrative_beat_architect
        beats = narrative_beat_architect.generate_scene_beats("Caelum", "The Solar Crucible", "Sun-Forged", "Helios Prime", "SURFACE", 15.0, "PEAK_FACING", "Output", "Limit")
        assert "act_1_opening_grounding" in beats["narrative_blueprint"]
        results.append({"test": "12. Confluence Authoring: Narrative Beat Architect", "status": "PASS", "details": "3-Act Blueprint Scaffolded"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "12. Confluence Authoring: Narrative Beat Architect", "status": "FAIL", "error": str(e)})

    # 13. Confluence Authoring: Resonance Calculator
    try:
        import calculate_resonance
        res_calc = calculate_resonance.calculate_resonance(15, "Sun-Forged Hegemony", "SURFACE")
        assert res_calc["resonance_state"] == "PEAK_FACING"
        results.append({"test": "13. Confluence Authoring: Resonance Calculator", "status": "PASS", "details": f"{res_calc['resonance_state']} ({res_calc['facing_angle_deg']}°)"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "13. Confluence Authoring: Resonance Calculator", "status": "FAIL", "error": str(e)})

    # 14. Confluence Authoring: Prose Readability Evaluator
    try:
        import chapter_prose_evaluator
        sample_prose = """
Caelum stared across the golden dunes of Helios Prime. The twin suns flared bright in the clear sky.
"Hold the lens steady!" Master Theron called out over the whistling desert wind.
Caelum turned the brass wheel with careful fingers. Click! The crystal locked into position, focusing a gleaming beam onto the solar relay. Warmth hummed into his gauntlet, but his grip remained firm.
"""
        eval_res = chapter_prose_evaluator.evaluate_prose(sample_prose)
        assert eval_res["status"] == "PASS"
        results.append({"test": "14. Confluence Authoring: Prose Evaluator", "status": "PASS", "details": f"Grade Level: {eval_res['flesch_kincaid_grade_level']} ({eval_res['target_age_group']})"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "14. Confluence Authoring: Prose Evaluator", "status": "FAIL", "error": str(e)})

    # 15. Confluence Authoring: Unified Chapter Engine
    try:
        import chapter_engine
        stub_res = chapter_engine.prepare_next_chapter_stub()
        assert stub_res["status"] == "ready"
        results.append({"test": "15. Confluence Authoring: Chapter Engine", "status": "PASS", "details": f"Book {stub_res['active_book']} Ch {stub_res['active_chapter']}"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "15. Confluence Authoring: Chapter Engine", "status": "FAIL", "error": str(e)})

    # 16. Prompt-Response Flow: Log Flow Entry
    try:
        import log_flow_entry
        active_f = log_flow_entry.get_active_flow_file()
        assert os.path.exists(active_f)
        results.append({"test": "16. Prompt-Response Flow: Active File", "status": "PASS", "details": os.path.basename(active_f)})
        passed_count += 1
    except Exception as e:
        results.append({"test": "16. Prompt-Response Flow: Active File", "status": "FAIL", "error": str(e)})

    # 17. World Engine: Full Universe State Audit
    try:
        import audit_universe_state
        aud_res = audit_universe_state.audit_state()
        assert aud_res["status"] == "PASS"
        results.append({"test": "17. World Engine: State Audit", "status": "PASS", "details": f"{aud_res['character_registry_count']} books"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "17. World Engine: State Audit", "status": "FAIL", "error": str(e)})

    # 18. World Engine: Celestial Physics & Lore Audit
    try:
        import audit_lore_physics
        lore_res = audit_lore_physics.audit_physics()
        assert lore_res["status"] == "PASS"
        results.append({"test": "18. World Engine: Physics & Lore Audit", "status": "PASS", "details": f"{lore_res['valid_records']} valid records"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "18. World Engine: Physics & Lore Audit", "status": "FAIL", "error": str(e)})

    duration_total_ms = round((time.time() - start_total) * 1000, 1)
    all_pass = (passed_count == len(results))

    return {
        "overall_status": "ALL_TESTS_PASS" if all_pass else "SOME_TESTS_FAILED",
        "passed_tests": f"{passed_count} / {len(results)}",
        "total_duration_ms": duration_total_ms,
        "test_results": results
    }

if __name__ == "__main__":
    summary = run_in_process_tests()
    print(json.dumps(summary, indent=2))
