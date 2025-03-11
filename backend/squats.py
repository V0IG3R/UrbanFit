# backend/squats.py
import numpy as np
import json
from state import exercise_state

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
         angle = 360 - angle
    return angle

with open("exercises/squats/calibration/squat_calibration.txt", "r") as f:
    calib = json.load(f)
knee_top_cal = calib.get("knee_angle_top", 160)
knee_bottom_cal = calib.get("knee_angle_bottom", 100)
trunk_top_cal = calib.get("trunk_angle_top", 170)
trunk_bottom_cal = calib.get("trunk_angle_bottom", 150)

def process_landmarks(landmarks, tolerance):
    try:
        # Use indices: 23: left hip, 25: left knee, 27: left ankle, 11: left shoulder.
        hip = [landmarks[23]['x'], landmarks[23]['y']]
        knee = [landmarks[25]['x'], landmarks[25]['y']]
        ankle = [landmarks[27]['x'], landmarks[27]['y']]
        shoulder = [landmarks[11]['x'], landmarks[11]['y']]
    except Exception:
        return {"error": "Insufficient landmarks data."}

    knee_angle = calculate_angle(hip, knee, ankle)
    trunk_angle = calculate_angle(shoulder, hip, knee)

    state = exercise_state.get("squats", {
        "counter": 0,
        "stage": "up",
        "repCounted": False,
        "currentMinKnee": None,
        "currentMinTrunk": None,
        "feedback": ""
    })
    stage = state.get("stage", "up")
    counter = state.get("counter", 0)
    rep_counted = state.get("repCounted", False)
    current_min_knee = state.get("currentMinKnee")
    current_min_trunk = state.get("currentMinTrunk")
    feedback = state.get("feedback", "")

    if stage == "up":
        if knee_angle > (knee_top_cal - tolerance) and trunk_angle > (trunk_top_cal - tolerance):
            stage = "up"
            rep_counted = False
        if knee_angle < (knee_bottom_cal + tolerance) and trunk_angle < (trunk_bottom_cal + tolerance) and stage == "up":
            stage = "down"
            current_min_knee = knee_angle
            current_min_trunk = trunk_angle
            feedback = "Descending..."
    elif stage == "down":
        if current_min_knee is None or knee_angle < current_min_knee:
            current_min_knee = knee_angle
        if current_min_trunk is None or trunk_angle < current_min_trunk:
            current_min_trunk = trunk_angle
        feedback = "At bottom position"
        if knee_angle > (knee_top_cal - tolerance) and trunk_angle > (trunk_top_cal - tolerance) and not rep_counted:
            if (abs(current_min_knee - knee_bottom_cal) <= tolerance and 
                abs(current_min_trunk - trunk_bottom_cal) <= tolerance):
                counter += 1
                feedback = "Good rep!"
            else:
                feedback = "Incorrect rep! Adjust posture."
            rep_counted = True
            stage = "up"
            current_min_knee = None
            current_min_trunk = None

    new_state = {
        "counter": counter,
        "stage": stage,
        "repCounted": rep_counted,
        "currentMinKnee": current_min_knee,
        "currentMinTrunk": current_min_trunk,
        "feedback": feedback
    }
    exercise_state["squats"] = new_state
    return new_state
