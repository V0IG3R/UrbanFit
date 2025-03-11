# backend/bicep_curls.py
import numpy as np
import json
from state import exercise_state

def calculate_angle(a, b, c):
    """Calculate the angle (in degrees) at point b given three points a, b, and c."""
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Load calibration thresholds (adjust the file path as needed)
with open("exercises/bicep_curls/calibration/bicep_curl_calibration.txt", "r") as f:
    calib = json.load(f)
elbow_top_cal = calib.get("elbow_angle_top", 160)
elbow_bottom_cal = calib.get("elbow_angle_bottom", 30)
posture_bottom_cal = calib.get("posture_angle_bottom", 40)

def process_landmarks(landmarks, tolerance):
    try:
        # Use MediaPipe landmark indices: 11: left shoulder, 13: left elbow, 15: left wrist, 23: left hip.
        shoulder = [landmarks[11]['x'], landmarks[11]['y']]
        elbow = [landmarks[13]['x'], landmarks[13]['y']]
        wrist = [landmarks[15]['x'], landmarks[15]['y']]
        hip = [landmarks[23]['x'], landmarks[23]['y']]
    except Exception:
        return {"error": "Insufficient landmarks data."}

    current_elbow = calculate_angle(shoulder, elbow, wrist)
    current_posture = calculate_angle(shoulder, elbow, hip)

    state = exercise_state.get("bicep_curls", {"repCount": 0, "stage": "down", "feedback": "N/A"})
    stage = state.get("stage", "down")
    counter = state.get("repCount", 0)

    if current_elbow > (elbow_top_cal - tolerance):
        stage = "down"
    if current_elbow < (elbow_bottom_cal + tolerance) and stage == "down":
        stage = "up"
        counter += 1

    posture_feedback = (
        "Good posture" if stage == "down" and abs(current_posture - posture_bottom_cal) <= tolerance
        else "Bad posture" if stage == "down" else "N/A"
    )

    new_state = {"repCount": counter, "stage": stage, "feedback": posture_feedback}
    exercise_state["bicep_curls"] = new_state
    return new_state
