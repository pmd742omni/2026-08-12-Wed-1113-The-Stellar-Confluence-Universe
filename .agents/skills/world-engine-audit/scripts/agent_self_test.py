#!/usr/bin/env python3
"""
Master 25-Point Agent Regression & Sanity Suite for The Stellar Confluence Universe
Executes in-process unit, integration, simulation, audio cadence, and publishing diagnostics
across all 5 skills and 25+ modules in under 200 milliseconds.
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
        results.append({"test": "4. Universe State: Ephemeris Propagation", "status": "PASS", "details": "Propagated 74 chars"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "4. Universe State: Ephemeris Propagation", "status": "FAIL", "error": str(e)})

    # 5. Universe State: Cosmic Event Bus
    try:
        import cosmic_event_bus
        ev_log = cosmic_event_bus.log_event("BEACON_PULSE", "Book 04", "[15, 6, 0]", 5.0, 100, 10, "Test Solar Flare")
        ev_check = cosmic_event_bus.check_hazards("[12, 5, 1]", 105)
        assert ev_check["active_hazard_count"] >= 1
        results.append({"test": "5. Universe State: Cosmic Event Bus", "status": "PASS", "details": f"Intensity: {ev_check['hazards'][0]['hazard_intensity']}"})
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

    # 10. Universe State: Character Mesh Graph & Mentors
    try:
        import character_mesh_graph
        mesh = character_mesh_graph.get_character_mesh(1)
        assert "mentor" in mesh["mesh"] and len(mesh["mesh"]["allies"]) >= 1
        results.append({"test": "10. Universe State: Character Mesh", "status": "PASS", "details": f"Mentor: {mesh['mesh']['mentor']}"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "10. Universe State: Character Mesh", "status": "FAIL", "error": str(e)})

    # 11. Universe State: Subspace Broadcast Network (News Feed)
    try:
        import galactic_broadcast_feed
        feed = galactic_broadcast_feed.get_broadcast_feed()
        assert feed["total_bulletins"] >= 1
        results.append({"test": "11. Universe State: Broadcast News Feed", "status": "PASS", "details": f"{feed['total_bulletins']} bulletins streamed"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "11. Universe State: Broadcast News Feed", "status": "FAIL", "error": str(e)})

    # 12. Universe State: Cockpit Radio Intercept
    try:
        import galactic_broadcast_feed
        radio = galactic_broadcast_feed.generate_radio_intercept(1)
        assert len(radio["transcript"]) >= 2
        results.append({"test": "12. Universe State: Cockpit Radio Intercept", "status": "PASS", "details": radio["channel"]})
        passed_count += 1
    except Exception as e:
        results.append({"test": "12. Universe State: Cockpit Radio Intercept", "status": "FAIL", "error": str(e)})

    # 13. Confluence Wavefront: 3D Wave Physics
    try:
        import confluence_wave_physics
        w_state = confluence_wave_physics.calculate_wavefront_state("[10, 5, 0]", 100.0)
        assert 0.5 <= w_state["wave_intensity_factor"] <= 1.5
        results.append({"test": "13. Confluence Wavefront: Wave Physics", "status": "PASS", "details": f"Phase: {w_state['wave_phase_degrees']}° (Intensity: {w_state['wave_intensity_factor']})"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "13. Confluence Wavefront: Wave Physics", "status": "FAIL", "error": str(e)})

    # 14. Confluence Wavefront: Relativistic Doppler Shift
    try:
        import confluence_wave_physics
        d_state = confluence_wave_physics.calculate_wavefront_state("[10, 5, 0]", 100.0, velocity_vec="[0, 2, 0]")
        assert d_state["doppler_shift_factor"] > 1.0
        results.append({"test": "14. Confluence Wavefront: Doppler Shift", "status": "PASS", "details": f"Doppler factor: {d_state['doppler_shift_factor']} ({d_state['observed_frequency_mhz']} MHz)"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "14. Confluence Wavefront: Doppler Shift", "status": "FAIL", "error": str(e)})

    # 15. Confluence Authoring: Faction Matrix
    try:
        import faction_matrix
        f_prof = faction_matrix.get_faction_profile("Comet-Riders")
        assert "SUBLIMATION SURGE" in f_prof["profile"]["peak_facing"]["buff"]
        results.append({"test": "15. Confluence Authoring: Faction Matrix", "status": "PASS", "details": f_prof['matched_name']})
        passed_count += 1
    except Exception as e:
        results.append({"test": "15. Confluence Authoring: Faction Matrix", "status": "FAIL", "error": str(e)})

    # 16. Confluence Authoring: Faction Diplomacy & Tension Engine
    try:
        import faction_diplomacy_engine
        dip = faction_diplomacy_engine.get_diplomatic_relation("Sun-Forged Hegemony", "Void-Bound Monks")
        assert dip["stance"] == "OPEN_RIVALRY" and dip["tension_index"] > 80
        results.append({"test": "16. Confluence Authoring: Faction Diplomacy", "status": "PASS", "details": f"Sun vs Void: {dip['stance']} ({dip['tension_index']}/100)"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "16. Confluence Authoring: Faction Diplomacy", "status": "FAIL", "error": str(e)})

    # 17. Confluence Authoring: Narrative Beat Architect
    try:
        import narrative_beat_architect
        beats = narrative_beat_architect.generate_scene_beats("Caelum", "The Solar Crucible", "Sun-Forged", "Helios Prime", "SURFACE", 15.0, "PEAK_FACING", "Output", "Limit")
        assert "act_1_opening_grounding" in beats["narrative_blueprint"]
        results.append({"test": "17. Confluence Authoring: Narrative Beat Architect", "status": "PASS", "details": "3-Act Blueprint Scaffolded"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "17. Confluence Authoring: Narrative Beat Architect", "status": "FAIL", "error": str(e)})

    # 18. Confluence Authoring: Resonance Calculator
    try:
        import calculate_resonance
        res_calc = calculate_resonance.calculate_resonance(15, "Sun-Forged Hegemony", "SURFACE")
        assert res_calc["resonance_state"] == "PEAK_FACING"
        results.append({"test": "18. Confluence Authoring: Resonance Calculator", "status": "PASS", "details": f"{res_calc['resonance_state']} ({res_calc['facing_angle_deg']}°)"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "18. Confluence Authoring: Resonance Calculator", "status": "FAIL", "error": str(e)})

    # 19. Confluence Authoring: Autonomous Story Generator
    try:
        import story_generator
        draft = story_generator.generate_full_chapter_prose(1, 1, save=False)
        assert draft["status"] == "drafted" and draft["total_words"] > 200
        results.append({"test": "19. Confluence Authoring: Story Generator", "status": "PASS", "details": f"{draft['total_words']} words drafted"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "19. Confluence Authoring: Story Generator", "status": "FAIL", "error": str(e)})

    # 20. Confluence Authoring: Anthology & Manuscript Compiler
    try:
        import anthology_compiler
        comp = anthology_compiler.compile_book_manuscript(1)
        assert comp["status"] == "compiled" and os.path.exists(comp["manuscript_file"])
        results.append({"test": "20. Confluence Authoring: Manuscript Compiler", "status": "PASS", "details": f"Compiled {comp['total_chapters']} chapters"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "20. Confluence Authoring: Manuscript Compiler", "status": "FAIL", "error": str(e)})

    # 21. Confluence Authoring: Prose Readability & Audio Cadence Evaluator
    try:
        import chapter_prose_evaluator
        sample_prose = """
The twin suns of Helios Prime climbed steadily into the copper sky, casting long, sharp shadows across the shifting sands.
Caelum adjusted the heavy bronze visor over his eyes. Even through the tinted glass, the horizon sparkled with dazzling light.
"Watch your heat gauge, Caelum!" called out Master Theron from the observatory balcony. His old voice was gravelly but kind. "At this morning angle, the radiant energy is eager to leap into our lenses."
"I hear you, Master!" Caelum shouted back with a grin, wiping a bead of sweat from his chin. "Slow and steady. Like turning the great waterwheel."
"""
        eval_res = chapter_prose_evaluator.evaluate_prose(sample_prose)
        assert eval_res["status"] == "PASS" and "audio_cadence" in eval_res
        results.append({"test": "21. Confluence Authoring: Readability & Cadence", "status": "PASS", "details": f"Grade: {eval_res['flesch_kincaid_grade_level']} | StdDev: {eval_res['audio_cadence']['sentence_length_std_dev']}"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "21. Confluence Authoring: Readability & Cadence", "status": "FAIL", "error": str(e)})

    # 22. Confluence Authoring: Unified Chapter Engine
    try:
        import chapter_engine
        stub_res = chapter_engine.prepare_next_chapter_stub()
        assert stub_res["status"] == "ready"
        results.append({"test": "22. Confluence Authoring: Chapter Engine", "status": "PASS", "details": f"Book {stub_res['active_book']} Ch {stub_res['active_chapter']}"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "22. Confluence Authoring: Chapter Engine", "status": "FAIL", "error": str(e)})

    # 23. Confluence Authoring: Universe Simulation Loop
    try:
        import universe_simulation_loop
        sim = universe_simulation_loop.run_simulation(steps=1, dry_run=True)
        assert sim["simulation_status"] == "COMPLETED"
        results.append({"test": "23. Confluence Authoring: Simulation Loop", "status": "PASS", "details": f"Simulated {sim['total_steps_executed']} step(s) (Dry Run)"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "23. Confluence Authoring: Simulation Loop", "status": "FAIL", "error": str(e)})

    # 24. World Engine: Full Universe State Audit
    try:
        import audit_universe_state
        aud_res = audit_universe_state.audit_state()
        assert aud_res["status"] == "PASS"
        results.append({"test": "24. World Engine: State Audit", "status": "PASS", "details": f"{aud_res['character_registry_count']} books"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "24. World Engine: State Audit", "status": "FAIL", "error": str(e)})

    # 25. World Engine: Celestial Physics & Lore Audit
    try:
        import audit_lore_physics
        lore_res = audit_lore_physics.audit_physics()
        assert lore_res["status"] == "PASS"
        results.append({"test": "25. World Engine: Physics & Lore Audit", "status": "PASS", "details": f"{lore_res['valid_records']} valid records"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "25. World Engine: Physics & Lore Audit", "status": "FAIL", "error": str(e)})

    # 26. Universe State: Multi-Book Cross Encounter Engine
    try:
        import multi_book_sync_engine
        enc_res = multi_book_sync_engine.detect_encounters(25.0)
        assert enc_res["status"] == "SCANNED"
        results.append({"test": "26. Universe State: Cross Encounter Engine", "status": "PASS", "details": f"{enc_res['total_encounters_detected']} encounters detected"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "26. Universe State: Cross Encounter Engine", "status": "FAIL", "error": str(e)})

    # 27. Confluence Authoring: Resonance Artifact & Power Consumption Engine
    try:
        import resonance_artifact_engine
        art_res = resonance_artifact_engine.calculate_artifact_performance("SOLAR_LENS", 15.0)
        assert art_res["resonance_zone"] == "PEAK_FACING" and art_res["power_output_kw"] > 0
        results.append({"test": "27. Confluence Authoring: Artifact Engine", "status": "PASS", "details": f"{art_res['artifact_type']}: {art_res['power_output_kw']} kW (Risk: {art_res['overheat_risk_pct']}%)"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "27. Confluence Authoring: Artifact Engine", "status": "FAIL", "error": str(e)})

    # 28. Confluence Authoring: Sensory Soundscape & Audio Director
    try:
        import sensory_audio_director
        aud_dir = sensory_audio_director.analyze_soundscape("The golden lens hummed with a dazzling beam while a low clack echoed.")
        assert aud_dir["status"] == "ANALYZED" and len(aud_dir["audio_cues_detected"]) >= 1
        results.append({"test": "28. Confluence Authoring: Sensory Audio Director", "status": "PASS", "details": f"Vibe: {aud_dir['recommended_color_vibe']} | Score: {aud_dir['sensory_richness_score']}"})
        passed_count += 1
    except Exception as e:
        results.append({"test": "28. Confluence Authoring: Sensory Audio Director", "status": "FAIL", "error": str(e)})

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
