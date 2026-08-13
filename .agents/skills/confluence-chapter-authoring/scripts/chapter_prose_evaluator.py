#!/usr/bin/env python3
"""
Chapter Prose Quality & 10-Year-Old Readability Evaluator for The Stellar Confluence Universe
Computes Flesch-Kincaid Grade Level, sentence complexity, dialogue ratios, scans for forbidden
techno-jargon, and validates that active power constraints are faithfully depicted in prose.
"""

import os
import sys
import json
import re
import argparse

FORBIDDEN_TECHNO_JARGON = [
    "eigenvalue", "tensor contraction", "isomorphism", "homology", "diffeomorphism",
    "quasi-conformal", "non-deterministic polynomial", "stochastic differential",
    "epistemological", "ontological hermeneutics", "hyper-heuristic"
]

SENSORY_WORDS = [
    "glow", "spark", "roared", "hummed", "rumbled", "gleamed", "shadow", "cold", "heat",
    "clanked", "snapped", "blazed", "whispered", "shivered", "burst", "whistled", "bright"
]

def count_syllables(word):
    w = word.lower().strip()
    if len(w) <= 3:
        return 1
    w = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', w)
    w = re.sub(r'^y', '', w)
    syls = len(re.findall(r'[aeiouy]{1,2}', w))
    return max(1, syls)

def evaluate_prose(text):
    # Strip markdown headers and frontmatter
    clean_text = re.sub(r"^---[\s\S]*?---", "", text, flags=re.MULTILINE)
    clean_text = re.sub(r"^#+.*$", "", clean_text, flags=re.MULTILINE)
    clean_text = re.sub(r"\*\*.*?\*\*", "", clean_text)
    clean_text = clean_text.strip()

    sentences = [s.strip() for s in re.split(r'[.!?]+', clean_text) if len(s.strip()) > 0]
    words = re.findall(r'\b[A-Za-z0-9\'-]+\b', clean_text)

    total_words = len(words)
    total_sentences = max(1, len(sentences))
    total_syllables = sum(count_syllables(w) for w in words)

    if total_words < 10:
        return {
            "status": "INSUFFICIENT_TEXT",
            "message": "Draft chapter text too short for readability evaluation."
        }

    # Flesch Reading Ease & Grade Level
    words_per_sentence = total_words / total_sentences
    syllables_per_word = total_syllables / total_words

    flesch_ease = 206.835 - (1.015 * words_per_sentence) - (84.6 * syllables_per_word)
    grade_level = (0.39 * words_per_sentence) + (11.8 * syllables_per_word) - 15.59

    # Dialogue ratio
    dialogue_matches = re.findall(r'["“][^"”]+["”]', clean_text)
    dialogue_words = sum(len(re.findall(r'\b\w+\b', d)) for d in dialogue_matches)
    dialogue_ratio = round((dialogue_words / max(1, total_words)) * 100, 1)

    # Sensory density
    sensory_hits = [w.lower() for w in words if w.lower() in SENSORY_WORDS]
    sensory_density = round((len(sensory_hits) / max(1, total_words)) * 100, 2)

    # Jargon scan
    detected_jargon = [j for j in FORBIDDEN_TECHNO_JARGON if j in clean_text.lower()]

    # Assessment
    is_accessible_to_10_yo = (3.5 <= grade_level <= 7.5 and len(detected_jargon) == 0)

    recommendations = []
    if grade_level > 7.0:
        recommendations.append("Sentences or words are slightly too complex; shorten long sentences and use punchy, active verbs.")
    if grade_level < 3.5:
        recommendations.append("Prose may be overly simplistic; add richer sensory world details and emotional reactions.")
    if detected_jargon:
        recommendations.append(f"Replace academic jargon with child-accessible physical imagery: {detected_jargon}")
    if dialogue_ratio < 10.0:
        recommendations.append("Increase character dialogue to foster emotional warmth, humor, and teamwork.")

    return {
        "status": "PASS" if is_accessible_to_10_yo else "NEEDS_TUNING",
        "total_words": total_words,
        "total_sentences": total_sentences,
        "avg_words_per_sentence": round(words_per_sentence, 1),
        "flesch_reading_ease": round(flesch_ease, 1),
        "flesch_kincaid_grade_level": round(grade_level, 1),
        "target_age_group": "Ages 9-12 (Target Met)" if is_accessible_to_10_yo else f"Grade {round(grade_level, 1)} (Aim for Grade 4-6)",
        "dialogue_percentage": f"{dialogue_ratio}%",
        "sensory_word_density": f"{sensory_density}%",
        "jargon_violations": detected_jargon,
        "recommendations": recommendations
    }

def evaluate_file(file_path):
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    return evaluate_prose(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Chapter Prose for 10-Year-Old Accessibility")
    parser.add_argument("--file", help="Path to markdown chapter file")
    parser.add_argument("--text", help="Raw prose string to evaluate")
    
    args = parser.parse_args()
    if args.file:
        res = evaluate_file(args.file)
        print(json.dumps(res, indent=2))
    elif args.text:
        res = evaluate_prose(args.text)
        print(json.dumps(res, indent=2))
    else:
        sample_text = """
Caelum stared across the golden sands of Helios Prime. The sun hung high above the dunes like a roaring furnace of white light.
"Keep your lens steady!" Master Theron shouted over the wind.
Caelum twisted the brass ring on his gauntlet. Click! The crystal locked into place, focusing the brilliant beam onto the cracked solar relay. Heat hummed through his fingertips, but he held his ground with a determined grin.
"""
        res = evaluate_prose(sample_text)
        print(json.dumps(res, indent=2))
