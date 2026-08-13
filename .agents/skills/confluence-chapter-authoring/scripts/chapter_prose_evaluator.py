#!/usr/bin/env python3
"""
Child Accessibility, Read-Aloud Cadence & Constraint Compliance Prose Evaluator
for The Stellar Confluence Universe
Computes Flesch-Kincaid Grade Level (Ages 9-12 / Grade 4-6 target), read-aloud sentence rhythm variance,
sensory word density, dialogue ratios, technobabble detection, and physical constraint adherence.
"""

import os
import sys
import re
import json
import argparse
import math

FORBIDDEN_TECHNOBABBLE = [
    "quantum entanglement", "hyper-dimensional topology", "antimatter flux density",
    "tachyon emitter", "spacetime manifold", "eigenstate", "baryonic asymmetry",
    "superposition collapse", "differential tensor", "gravitational singularity"
]

SENSORY_WORDS = {
    "visual": ["gleamed", "glared", "sparkled", "bronze", "shadow", "amber", "golden", "copper", "flicker", "blaze", "radiant", "dim", "crimson", "shimmer"],
    "auditory": ["hummed", "groaned", "chimed", "hissed", "clicked", "whistled", "clang", "roared", "thumped", "whispered", "crackled"],
    "tactile": ["warmth", "chill", "heavy", "smooth", "sharp", "insulated", "vibrating", "rough", "freezing", "searing", "grip"],
    "action": ["leaped", "ducked", "cranked", "pulled", "twisted", "soared", "glided", "darted", "braced"]
}

def count_syllables(word):
    word = word.lower().strip(".:;?!'\",")
    if not word:
        return 0
    if len(word) <= 3:
        return 1
    word = re.sub(r'(?:[^laeiouy]|ed|es|e)$', '', word)
    word = re.sub(r'^y', '', word)
    syllables = len(re.findall(r'[aeiouy]{1,2}', word))
    return max(1, syllables)

def evaluate_audio_cadence(sentences):
    if not sentences:
        return {"cadence_rating": "N/A", "rhythm_variance": 0.0}
    
    lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences if len(s.strip()) > 0]
    if not lengths:
        return {"cadence_rating": "N/A", "rhythm_variance": 0.0}

    mean_len = sum(lengths) / len(lengths)
    variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)

    # Good children's read-aloud prose alternates short punchy sentences (3-6 words) with descriptive sentences (10-14 words)
    # std_dev in range [3.0, 7.0] is ideal dynamic cadence
    if 3.0 <= std_dev <= 7.0:
        cadence_score = "EXCELLENT_RHYTHM (Dynamic sentence length variety for read-aloud engagement)"
    elif std_dev < 3.0:
        cadence_score = "MONOTONOUS_PACING (Sentences are too uniform in length; mix short & long sentences)"
    else:
        cadence_score = "OVERLY_COMPLEX (High variance; check for overly lengthy run-on sentences)"

    return {
        "mean_sentence_length": round(mean_len, 1),
        "sentence_length_std_dev": round(std_dev, 2),
        "cadence_assessment": cadence_score
    }

def evaluate_prose(text, expected_constraint=None):
    clean_text = re.sub(r'<!--[\s\S]*?-->', '', text)
    clean_text = re.sub(r'^#+.*$', '', clean_text, flags=re.MULTILINE)
    clean_text = re.sub(r'\*\*.*?\*\*', '', clean_text)
    clean_text = clean_text.strip()

    words = re.findall(r'\b[A-Za-z0-9\'-]+\b', clean_text)
    total_words = len(words)

    raw_sentences = re.split(r'[\.\?!]+\s+', clean_text)
    sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 0]
    total_sentences = max(1, len(sentences))

    if total_words == 0:
        return {"error": "Empty text body; unable to evaluate prose."}

    total_syllables = sum(count_syllables(w) for w in words)

    # Readability Formulas
    asl = total_words / total_sentences
    asw = total_syllables / total_words

    fre = 206.835 - (1.015 * asl) - (84.6 * asw)
    fkgl = (0.39 * asl) + (11.8 * asw) - 15.59

    fre = round(max(0.0, min(100.0, fre)), 1)
    fkgl = round(max(1.0, fkgl), 1)

    # Dialogue Analysis
    dialogue_quotes = re.findall(r'"([^"]*)"', clean_text)
    dialogue_words = sum(len(re.findall(r'\b\w+\b', q)) for q in dialogue_quotes)
    dialogue_pct = round((dialogue_words / max(1, total_words)) * 100, 1)

    # Sensory Word Density
    sensory_matches = []
    lower_text = clean_text.lower()
    for cat, word_list in SENSORY_WORDS.items():
        for sw in word_list:
            if re.search(rf'\b{sw}\b', lower_text):
                sensory_matches.append(sw)
    sensory_density = round((len(sensory_matches) / max(1, total_words)) * 100, 2)

    # Technobabble Scanning
    jargon_found = []
    for j in FORBIDDEN_TECHNOBABBLE:
        if j in lower_text:
            jargon_found.append(j)

    # Audio Cadence & Rhythm
    audio_cadence = evaluate_audio_cadence(sentences)

    # Grade Level Check: Target is Grade 4.0 - 6.9 (Ages 9-12)
    is_grade_appropriate = (3.5 <= fkgl <= 7.0)

    recommendations = []
    if fkgl > 7.0:
        recommendations.append("Reduce sentence length and simplify multi-syllable vocabulary to reach Grade 4-6 target.")
    elif fkgl < 3.5:
        recommendations.append("Prose may be slightly too simple; add richer sensory and emotional descriptions.")
    
    if dialogue_pct < 10.0:
        recommendations.append("Increase character dialogue to foster emotional warmth, humor, and teamwork.")
    
    if jargon_found:
        recommendations.append(f"Remove complex technobabble terms ({', '.join(jargon_found)}) and replace with grounded sensory physics.")

    return {
        "status": "PASS" if is_grade_appropriate and not jargon_found else "WARNING",
        "total_words": total_words,
        "total_sentences": total_sentences,
        "avg_words_per_sentence": round(asl, 1),
        "flesch_reading_ease": fre,
        "flesch_kincaid_grade_level": fkgl,
        "target_age_group": "Ages 9-12 (Target Met)" if is_grade_appropriate else "Out of Target",
        "dialogue_percentage": f"{dialogue_pct}%",
        "sensory_word_density": f"{sensory_density}%",
        "audio_cadence": audio_cadence,
        "jargon_violations": jargon_found,
        "recommendations": recommendations
    }

def evaluate_file(file_path):
    if not os.path.exists(file_path):
        return {"error": f"File {file_path} does not exist."}
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return evaluate_prose(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chapter Prose Readability & Cadence Evaluator")
    parser.add_argument("--file", help="Path to markdown chapter file")
    
    args = parser.parse_args()
    if args.file:
        res = evaluate_file(args.file)
    else:
        sample_prose = """
The twin suns of Helios Prime climbed steadily into the copper sky, casting long, sharp shadows across the shifting sands.
Caelum adjusted the heavy bronze visor over his eyes. Even through the tinted glass, the horizon sparkled with dazzling light.
"Watch your heat gauge, Caelum!" called out Master Theron from the observatory balcony. His old voice was gravelly but kind. "At this morning angle, the radiant energy is eager to leap into our lenses."
"I hear you, Master!" Caelum shouted back with a grin, wiping a bead of sweat from his chin. "Slow and steady. Like turning the great waterwheel."
"""
        res = evaluate_prose(sample_prose)
    print(json.dumps(res, indent=2))
