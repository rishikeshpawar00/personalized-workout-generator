import streamlit as st
import random
import json

# -------------------------------
# Exercise data (shortened here, but you can paste your full EXERCISES list)
# -------------------------------
EXERCISES = [
    {"name": "Back Squat", "tags": ["legs"], "type": "compound"},
    {"name": "Deadlift", "tags": ["pull"], "type": "compound"},
    {"name": "Bench Press", "tags": ["push"], "type": "compound"},
    {"name": "Pull-up", "tags": ["pull"], "type": "compound"},
    {"name": "Overhead Press", "tags": ["push"], "type": "compound"},
    {"name": "Biceps Curl", "tags": ["pull"], "type": "accessory"},
    {"name": "Lateral Raise", "tags": ["push"], "type": "accessory"},
    {"name": "Plank", "tags": ["core"], "type": "core"},
    {"name": "Bike Intervals", "tags": ["conditioning"], "type": "conditioning"},
]

WARM_UPS = ["5 min light cardio", "Dynamic stretches", "Arm circles"]
COOL_DOWNS = ["Stretching", "Foam rolling", "Easy cardio"]

INTENSITY_GUIDE = {
    "beginner": {"compound_sets": 3, "accessory_sets": 2, "reps_strength": (5, 8), "reps_hypertrophy": (8, 12)},
    "intermediate": {"compound_sets": 4, "accessory_sets": 3, "reps_strength": (4, 6), "reps_hypertrophy": (6, 10)},
    "advanced": {"compound_sets": 5, "accessory_sets": 3, "reps_strength": (3, 5), "reps_hypertrophy": (5, 8)},
}

# -------------------------------
# Helper functions
# -------------------------------
def default_sets_reps(ex, level, goal):
    g = INTENSITY_GUIDE[level]
    if ex["type"] == "compound":
        reps = random.randint(*g["reps_strength"]) if goal == "strength" else random.randint(*g["reps_hypertrophy"])
        sets = g["compound_sets"]
    elif ex["type"] == "accessory":
        reps = random.randint(10, 15)
        sets = g["accessory_sets"]
    elif ex["type"] == "core":
        reps, sets = "45 sec hold", 3
    else:  # conditioning
        reps, sets = "30:30 x 8", 1
    return {"sets": sets, "reps": reps}

def generate_plan(goal, days, minutes, level):
    plan = []
    for w in range(4):  # 4 weeks
        week_days = []
        for d in range(days):
            random.shuffle(EXERCISES)
            exercises = EXERCISES[:min(5, len(EXERCISES))]
            day_plan = []
            for ex in exercises:
                sr = default_sets_reps(ex, level, goal)
                entry = {**ex, **sr}
                if w == 1 and ex["type"] == "accessory":
                    entry["sets"] += 1
                if w == 2 and ex["type"] in ("compound", "accessory") and isinstance(entry["reps"], int):
                    entry["reps"] += 2
                if w == 3 and ex["type"] in ("compound", "accessory"):
                    entry["note"] = "Increase load by ~5%"
                day_plan.append(entry)
            week_days.append(day_plan)
        plan.append(week_days)
    return plan

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🏋️ Personalized Workout Generator")

goal = st.selectbox("Primary goal:", ["strength", "hypertrophy", "fat_loss"])
days = st.slider("Days per week:", 2, 6, 3)
minutes = st.slider("Minutes per session:", 30, 90, 60)
level = st.selectbox("Fitness level:", ["beginner", "intermediate", "advanced"])

if st.button("Generate Plan"):
    plan = generate_plan(goal, days, minutes, level)
    st.subheader("Your 4-Week Workout Plan")
    st.write("**Warm-up:**", WARM_UPS)
    st.write("**Cool-down:**", COOL_DOWNS)

    for w, week in enumerate(plan, 1):
        st.markdown(f"### Week {w}")
        for d, day in enumerate(week, 1):
            st.markdown(f"**Day {d}:**")
            for item in day:
                note = f" | {item.get('note')}" if item.get("note") else ""
                st.write(f"- {item['name']} ({item['type']}) → {item['sets']} sets x {item['reps']}{note}")

    if st.checkbox("Export plan as JSON"):
        st.json(plan)
