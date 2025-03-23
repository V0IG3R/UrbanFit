import numpy as np
from state import exercise_state

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
         angle = 360 - angle
    return angle

def process_landmarks(landmarks, tolerance):
    angles = []
    # Attempt to get left-side landmarks: 23: hip, 25: knee, 27: ankle.
    try:
        left_hip = [landmarks[23]['x'], landmarks[23]['y']]
        left_knee = [landmarks[25]['x'], landmarks[25]['y']]
        left_ankle = [landmarks[27]['x'], landmarks[27]['y']]
        left_angle = calculate_angle(left_hip, left_knee, left_ankle)
        angles.append(left_angle)
    except Exception:
        pass

    # Attempt to get right-side landmarks: 24: hip, 26: knee, 28: ankle.
    try:
        right_hip = [landmarks[24]['x'], landmarks[24]['y']]
        right_knee = [landmarks[26]['x'], landmarks[26]['y']]
        right_ankle = [landmarks[28]['x'], landmarks[28]['y']]
        right_angle = calculate_angle(right_hip, right_knee, right_ankle)
        angles.append(right_angle)
    except Exception:
        pass

    if not angles:
        return {"error": "Insufficient landmarks data."}

    avg_angle = sum(angles) / len(angles)

    # Retrieve the current state for squats.
    state = exercise_state.get("squats", {
        "counter": 0,
        "stage": "up",
        "repCounted": False,
        "currentMinKnee": None,
        "currentMinTrunk": None,
        "feedback": "N/A"
    })
    stage = state.get("stage", "up")
    counter = state.get("counter", 0)

    # New squat logic using fixed thresholds.
    if avg_angle > 160:
        stage = "up"
    elif avg_angle < 100 and stage == "up":
        stage = "down"
        counter += 1

    # Reset unused state parameters.
    new_state = {
        "counter": counter,
        "stage": stage,
        "repCounted": False,
        "currentMinKnee": None,
        "currentMinTrunk": None,
        "feedback": "N/A"
    }
    exercise_state["squats"] = new_state
    return new_state
