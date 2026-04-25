import json
import os
import math

MODEL_FILE = "student_model.json"

# Skills we track (match those in problems.py)
SKILLS = ["basic_where", "comparison_operators", "group_by_aggregate", "null_handling"]

# Default BKT parameters (simplified)
# p_learn = probability of learning after an opportunity
# p_guess = probability of correct answer by chance
# p_slip = probability of incorrect answer despite mastery
PARAMS = {
    "basic_where": {"p_mastered": 0.2, "p_learn": 0.3, "p_guess": 0.2, "p_slip": 0.1},
    "comparison_operators": {"p_mastered": 0.2, "p_learn": 0.3, "p_guess": 0.2, "p_slip": 0.1},
    "group_by_aggregate": {"p_mastered": 0.1, "p_learn": 0.4, "p_guess": 0.25, "p_slip": 0.15},
    "null_handling": {"p_mastered": 0.1, "p_learn": 0.35, "p_guess": 0.2, "p_slip": 0.1},
}

def calculate_entropy(p):
    """Calculate Shannon entropy as uncertainty measure (0 = certain, 1 = uncertain)"""
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)

def calculate_confidence(count):
    """Calculate confidence as function of evidence (observations). Returns 0-1."""
    return min(0.95, count / (count + 5.0))

def load_model():
    if os.path.exists(MODEL_FILE):
        with open(MODEL_FILE, 'r') as f:
            model = json.load(f)
            # Ensure all skills have observation counts (backward compatibility)
            for skill in SKILLS:
                if skill not in model:
                    model[skill] = PARAMS[skill].copy()
                    model[skill]["observation_count"] = 0
                if "observation_count" not in model[skill]:
                    model[skill]["observation_count"] = 0
            return model
    else:
        # Initialize fresh model
        model = {}
        for skill in SKILLS:
            model[skill] = PARAMS[skill].copy()
            model[skill]["observation_count"] = 0
        return model

def save_model(model):
    with open(MODEL_FILE, 'w') as f:
        json.dump(model, f, indent=2)

def update_knowledge(model, problem_skills, was_correct):
    """Update mastery probabilities for all skills in the problem using BKT"""
    for skill in problem_skills:
        if skill not in model:
            continue
        p = model[skill]["p_mastered"]
        guess = model[skill]["p_guess"]
        slip = model[skill]["p_slip"]
        
        # Bayes' rule: probability of mastery given observed correctness
        if was_correct:
            p_mastered_given_correct = (p * (1 - slip)) / (p * (1 - slip) + (1 - p) * guess)
        else:
            p_mastered_given_incorrect = (p * slip) / (p * slip + (1 - p) * (1 - guess))
            p_mastered_given_correct = p_mastered_given_incorrect  # rename for clarity
        
        # Apply learning: after this attempt, student may learn
        p_learn = model[skill]["p_learn"]
        new_p = p_mastered_given_correct + (1 - p_mastered_given_correct) * p_learn
        model[skill]["p_mastered"] = min(1.0, new_p)
        model[skill]["observation_count"] += 1
        model[skill]["entropy"] = calculate_entropy(model[skill]["p_mastered"])
        model[skill]["confidence"] = calculate_confidence(model[skill]["observation_count"])
    
    save_model(model)
    return model

def get_next_problem(model, all_problems, completed_ids):
    """Select problem whose weakest skill has lowest mastery, not already completed"""
    # Find skill with lowest p_mastered
    weakest_skill = min(model.keys(), key=lambda s: model[s]["p_mastered"])
    
    # Find first incomplete problem that uses that skill
    for p in all_problems:
        if p["id"] in completed_ids:
            continue
        if weakest_skill in p.get("skills", []):
            return p["id"]
    # Fallback: any incomplete problem
    for p in all_problems:
        if p["id"] not in completed_ids:
            return p["id"]
    return None