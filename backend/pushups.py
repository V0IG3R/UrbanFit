# backend/pushups.py
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

with open("exercises/pushups/calibration/pushup_calibration.txt", "r") as f:
    calib = json.load(f)
elbow_top_cal = calib.get("elbow_angle_top", 160)
elbow_bottom_cal = calib.get("elbow_angle_bottom", 30)
alignment_top_cal = calib.get("alignment_angle_top", 180)
alignment_bottom_cal = calib.get("alignment_angle_bottom", 170)

def process_landmarks(landmarks, tolerance):
    try:
        # Use indices: 11: left shoulder, 13: left elbow, 15: left wrist, 23: left hip, 27: left ankle.
        shoulder = [landmarks[11]['x'], landmarks[11]['y']]
        elbow = [landmarks[13]['x'], landmarks[13]['y']]
        wrist = [landmarks[15]['x'], landmarks[15]['y']]
        hip = [landmarks[23]['x'], landmarks[23]['y']]
        ankle = [landmarks[27]['x'], landmarks[27]['y']]
    except Exception:
        return {"error": "Insufficient landmarks data."}

    current_elbow = calculate_angle(shoulder, elbow, wrist)
    current_alignment = calculate_angle(shoulder, hip, ankle)

    state = exercise_state.get("pushups", {"counter": 0, "stage": "up", "feedback": "N/A"})
    stage = state.get("stage", "up")
    counter = state.get("counter", 0)

    if stage == "up" and current_elbow < (elbow_bottom_cal + tolerance):
         stage = "down"
    elif stage == "down" and current_elbow > (elbow_top_cal - tolerance):
         stage = "up"
         counter += 1

    posture_feedback = "Good posture" if abs(current_alignment - alignment_bottom_cal) >= tolerance else "Bad posture"

    new_state = {"counter": counter, "stage": stage, "feedback": posture_feedback}
    exercise_state["pushups"] = new_state
    return new_state
