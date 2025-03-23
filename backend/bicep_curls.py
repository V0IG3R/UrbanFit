import numpy as np
from state import exercise_state

def calculate_angle(a, b, c):
    """
    Calculate the angle (in degrees) at point b given three points a, b, and c.
    """
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def process_landmarks(landmarks, tolerance=0.0):
    """
    Process the provided landmarks for bicep curl analysis using a backend state.
    
    Expects a dictionary of landmarks where keys are landmark indices and values are dictionaries
    with 'x' and 'y' coordinates.
    
    Returns a dictionary representing the updated exercise state including rep count, stage,
    feedback, and the average computed angle.
    """
    angles = []
    
    # Calculate left arm angle (shoulder: 11, elbow: 13, wrist: 15)
    try:
        left_shoulder = [landmarks[11]['x'], landmarks[11]['y']]
        left_elbow = [landmarks[13]['x'], landmarks[13]['y']]
        left_wrist = [landmarks[15]['x'], landmarks[15]['y']]
        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        angles.append(left_angle)
    except KeyError:
        pass

    # Calculate right arm angle (shoulder: 12, elbow: 14, wrist: 16)
    try:
        right_shoulder = [landmarks[12]['x'], landmarks[12]['y']]
        right_elbow = [landmarks[14]['x'], landmarks[14]['y']]
        right_wrist = [landmarks[16]['x'], landmarks[16]['y']]
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        angles.append(right_angle)
    except KeyError:
        pass

    if not angles:
        return {"error": "Insufficient landmarks data."}

    avg_angle = sum(angles) / len(angles)

    # Retrieve the current state for bicep_curls
    state = exercise_state.get("bicep_curls", {"repCount": 0, "stage": "down", "feedback": "N/A"})
    stage = state.get("stage", "down")
    counter = state.get("repCount", 0)

    # Debug: Log the average angle and current stage
    print(f"Average Angle: {avg_angle:.2f}°, Current Stage: {stage}")

    # Update stage and count based on bicep curl thresholds
    if avg_angle > 160:
        stage = "down"
    elif avg_angle < 60 and stage == "down":
        stage = "up"
        counter += 1

    new_state = {
        "repCount": counter,
        "stage": stage,
        "feedback": "N/A",
        "avg_angle": avg_angle
    }
    exercise_state["bicep_curls"] = new_state
    return new_state