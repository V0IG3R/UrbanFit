import numpy as np
from state import exercise_state

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
         angle = 360 - angle
    return angle

def process_landmarks(landmarks, tolerance):
    angles = []
    # Attempt to get left-side landmarks: 11: shoulder, 23: hip, 25: knee.
    try:
        left_shoulder = [landmarks[11]['x'], landmarks[11]['y']]
        left_hip = [landmarks[23]['x'], landmarks[23]['y']]
        left_knee = [landmarks[25]['x'], landmarks[25]['y']]
        left_angle = calculate_angle(left_shoulder, left_hip, left_knee)
        angles.append(left_angle)
    except Exception:
        pass

    # Attempt to get right-side landmarks: 12: shoulder, 24: hip, 26: knee.
    try:
        right_shoulder = [landmarks[12]['x'], landmarks[12]['y']]
        right_hip = [landmarks[24]['x'], landmarks[24]['y']]
        right_knee = [landmarks[26]['x'], landmarks[26]['y']]
        right_angle = calculate_angle(right_shoulder, right_hip, right_knee)
        angles.append(right_angle)
    except Exception:
        pass

    if not angles:
        return {"error": "Insufficient landmarks data."}

    avg_angle = sum(angles) / len(angles)

    # Retrieve the current state for sit-ups.
    state = exercise_state.get("situps", {"counter": 0, "stage": "up", "feedback": "N/A"})
    stage = state.get("stage", "up")
    counter = state.get("counter", 0)

    # New sit-up logic using fixed thresholds.
    if avg_angle > 160:
        stage = "down"
    elif avg_angle < 100 and stage == "down":
        stage = "up"
        counter += 1

    new_state = {"counter": counter, "stage": stage, "feedback": "N/A"}
    exercise_state["situps"] = new_state
    return new_state
