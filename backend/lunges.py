# backend/lunges.py
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

with open("exercises/lunges/calibration/lunge_calibration.txt", "r") as f:
    calib = json.load(f)
knee_top_cal = calib.get("knee_angle_top", 170)
knee_bottom_cal = calib.get("knee_angle_bottom", 90)
alignment_top_cal = calib.get("alignment_angle_top", 180)
alignment_bottom_cal = calib.get("alignment_angle_bottom", 150)

def process_landmarks(landmarks, tolerance):
    try:
        # Use indices: 23: left hip, 25: left knee, 27: left ankle, 11: left shoulder.
        hip = [landmarks[23]['x'], landmarks[23]['y']]
        knee = [landmarks[25]['x'], landmarks[25]['y']]
        ankle = [landmarks[27]['x'], landmarks[27]['y']]
        shoulder = [landmarks[11]['x'], landmarks[11]['y']]
    except Exception:
        return {"error": "Insufficient landmarks data."}

    current_knee = calculate_angle(hip, knee, ankle)
    current_alignment = calculate_angle(shoulder, hip, knee)

    state = exercise_state.get("lunges", {"counter": 0, "stage": "up", "feedback": "N/A"})
    stage = state.get("stage", "up")
    counter = state.get("counter", 0)
    posture_feedback = "N/A"

    if stage == "up" and current_knee < (knee_bottom_cal + tolerance):
        stage = "down"
    elif stage == "down" and current_knee > (knee_top_cal - tolerance):
        stage = "up"
        counter += 1

    if stage == "down":
        posture_feedback = "Good posture" if abs(current_alignment - alignment_bottom_cal) <= tolerance else "Bad posture"
    else:
        posture_feedback = "N/A"

    new_state = {"counter": counter, "stage": stage, "feedback": posture_feedback}
    exercise_state["lunges"] = new_state
    return new_state
