# backend/situps.py
import numpy as np
import json
from state import exercise_state

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0/np.pi)
    if angle > 180.0:
         angle = 360 - angle
    return angle

with open("exercises/situps/calibration/situp_calibration.txt", "r") as f:
    calib = json.load(f)
situp_top_cal = calib.get("situp_angle_top", 160)
situp_bottom_cal = calib.get("situp_angle_bottom", 100)
posture_bottom_cal = calib.get("posture_angle_bottom", 100)

def process_landmarks(landmarks, tolerance):
    try:
        # Use indices: 11: left shoulder, 23: left hip, 25: left knee.
        shoulder = [landmarks[11]['x'], landmarks[11]['y']]
        hip = [landmarks[23]['x'], landmarks[23]['y']]
        knee = [landmarks[25]['x'], landmarks[25]['y']]
    except Exception:
        return {"error": "Insufficient landmarks data."}

    current_angle = calculate_angle(shoulder, hip, knee)

    state = exercise_state.get("situps", {"counter": 0, "stage": "up", "feedback": "N/A"})
    stage = state.get("stage", "up")
    counter = state.get("counter", 0)

    if stage == "up" and current_angle > (situp_top_cal - tolerance):
         stage = "down"
    elif stage == "down" and current_angle < (situp_bottom_cal + tolerance):
         stage = "up"
         counter += 1

    posture_feedback = "Good posture" if stage == "down" and abs(current_angle - posture_bottom_cal) <= tolerance else "Bad posture" if stage == "down" else "N/A"

    new_state = {"counter": counter, "stage": stage, "feedback": posture_feedback}
    exercise_state["situps"] = new_state
    return new_state
