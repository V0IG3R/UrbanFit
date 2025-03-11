# backend/deadlifts.py
import numpy as np
import json
from state import exercise_state

def calculate_angle(a, b, c):
    """Calculate angle in degrees at point b."""
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

with open("exercises/deadlifts/calibration/deadlift_angles.txt", "r") as f:
    calib = json.load(f)
hip_angle_top_cal = calib.get("hip_angle_top", 154)
hip_angle_bottom_cal = calib.get("hip_angle_bottom", 58)
knee_angle_top_cal = calib.get("knee_angle_top", 165)
knee_angle_bottom_cal = calib.get("knee_angle_bottom", 94)

def process_landmarks(landmarks, tolerance):
    try:
        # MediaPipe landmark indices:
        # Left shoulder: 11, Right shoulder: 12, Left hip: 23, Right hip: 24,
        # Left knee: 25, Right knee: 26, Left ankle: 27, Right ankle: 28.
        left_shoulder = [landmarks[11]['x'], landmarks[11]['y']]
        right_shoulder = [landmarks[12]['x'], landmarks[12]['y']]
        left_hip = [landmarks[23]['x'], landmarks[23]['y']]
        right_hip = [landmarks[24]['x'], landmarks[24]['y']]
        left_knee = [landmarks[25]['x'], landmarks[25]['y']]
        right_knee = [landmarks[26]['x'], landmarks[26]['y']]
        left_ankle = [landmarks[27]['x'], landmarks[27]['y']]
        right_ankle = [landmarks[28]['x'], landmarks[28]['y']]
    except Exception:
        return {"error": "Insufficient landmarks data."}

    left_hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
    right_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
    hip_angle = (left_hip_angle + right_hip_angle) / 2

    left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
    right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
    knee_angle = (left_knee_angle + right_knee_angle) / 2

    state = exercise_state.get("deadlifts", {"repState": "up", "currentMinHip": None, "correctReps": 0, "incorrectReps": 0, "feedback": ""})
    rep_state = state.get("repState", "up")
    current_min_hip = state.get("currentMinHip")
    correct_reps = state.get("correctReps", 0)
    incorrect_reps = state.get("incorrectReps", 0)
    feedback = state.get("feedback", "")

    if rep_state == "up":
        if hip_angle < (hip_angle_bottom_cal + tolerance):
            rep_state = "down"
            current_min_hip = hip_angle
            feedback = "Descending..."
    elif rep_state == "down":
        if current_min_hip is None or hip_angle < current_min_hip:
            current_min_hip = hip_angle
        feedback = "Adjust form!" if abs(current_min_hip - hip_angle_bottom_cal) > tolerance else "At bottom"
        if hip_angle > (hip_angle_top_cal - tolerance):
            if abs(current_min_hip - hip_angle_bottom_cal) <= tolerance:
                correct_reps += 1
                feedback = "Good rep!"
            else:
                incorrect_reps += 1
                feedback = "Incorrect rep! Fix your form."
            rep_state = "up"
            current_min_hip = None

    new_state = {
        "repState": rep_state,
        "currentMinHip": current_min_hip,
        "correctReps": correct_reps,
        "incorrectReps": incorrect_reps,
        "feedback": feedback
    }
    exercise_state["deadlifts"] = new_state
    return new_state
