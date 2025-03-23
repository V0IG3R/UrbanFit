import numpy as np
import mediapipe as mp
from state import exercise_state

# Define the angle calculation function exactly as in your new code.
def calculate_angle(a, b, c):
    a = np.array(a)  # First point (shoulder)
    b = np.array(b)  # Mid point (elbow)
    c = np.array(c)  # End point (wrist)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Setup MediaPipe Pose for landmark indexing.
mp_pose = mp.solutions.pose

# Define the pushup process function.
def process_landmarks(landmarks, tolerance):
    """
    Process the provided landmarks for pushup detection using the new logic.
    
    Input:
      - landmarks: a list of MediaPipe Pose landmark objects
      - tolerance: numeric value to adjust sensitivity (kept for API consistency)
      
    Returns a dictionary with:
      - counter: int, the number of pushup repetitions counted
      - stage: str, the current stage ("up" or "down")
      - feedback: str, a string with the current elbow angle and stage
    """
    try:
        # Extract coordinates using MediaPipe landmark indices.
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    except Exception:
        return {"error": "Insufficient landmarks data."}
    
    # Calculate the elbow angle.
    angle = calculate_angle(shoulder, elbow, wrist)
    
    # Define threshold angles.
    max_angle = 160  # When the arm is fully extended ("up")
    min_angle = 30   # When the arm is bent ("down")
    
    # Retrieve or initialize pushup state.
    state = exercise_state.get("pushups", {"counter": 0, "stage": "up", "feedback": "N/A"})
    stage = state.get("stage", "up")
    counter = state.get("counter", 0)
    
    # Pushup counter logic based on the new code:
    if angle > max_angle:
        stage = "down"
    if angle < min_angle and stage == "down":
        stage = "up"
        counter += 1
    
    # Prepare feedback string.
    feedback = f"Angle: {round(angle, 1)} | Stage: {stage}"
    
    new_state = {"counter": counter, "stage": stage, "feedback": feedback}
    exercise_state["pushups"] = new_state
    return new_state
