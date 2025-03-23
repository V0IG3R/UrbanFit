import numpy as np
import pandas as pd
import pickle
import time
from landmarks import landmarks  # This should be a list of column names matching your model's features

# Load the pre-trained deadlift model.
model = pickle.load(open('deadlift.pkl', 'rb'))

# Separate state for deadlifts.
exercise_state = {
    "deadlifts": {
        "repCount": 0,
        "stage": "up",  # start with "up"
        "feedback": "N/A",
        "prob": 0.0,
        "last_update": time.time()
    }
}

def process_landmarks(landmarks_input, tolerance=0.0, reset_threshold=5.0):
    """
    Process the provided landmarks for deadlift analysis.
    
    Parameters:
        landmarks_input (list): List of landmark dictionaries.
                                Each dictionary should have keys 'x', 'y', 'z', and 'visibility'.
        tolerance (float): Reserved for any future threshold adjustments.
        reset_threshold (float): Time (in seconds) after which the rep count resets due to inactivity.
    
    Returns:
        dict: Updated exercise state containing:
              - repCount: Number of reps counted.
              - stage: Current stage ("up" or "down").
              - feedback: Feedback message.
              - prob: Maximum probability from the model prediction.
    """
    try:
        # Check for inactivity and reset if necessary
        current_time = time.time()
        state = exercise_state["deadlifts"]
        if current_time - state["last_update"] > reset_threshold:
            print("Long pause detected. Resetting rep count.")
            state["repCount"] = 0

        # Build the feature vector by flattening each landmark's x, y, z, and visibility values.
        row = []
        for lm in landmarks_input:
            row.extend([
                lm.get('x', 0),
                lm.get('y', 0),
                lm.get('z', 0),
                lm.get('visibility', 0)
            ])
        
        # Create a DataFrame with one row using the expected column order.
        X = pd.DataFrame([row], columns=landmarks)
        
        # Get model predictions.
        bodylang_prob = model.predict_proba(X)[0]
        bodylang_class = model.predict(X)[0]

        # Ensure predicted class is a lowercase string.
        if not isinstance(bodylang_class, str):
            bodylang_class = str(bodylang_class)
        bodylang_class = bodylang_class.lower()
        max_prob = float(np.max(bodylang_prob))

        # Detailed debug logging.
        print("---------- Debug Info ----------")
        print(f"Landmarks row: {row}")
        print(f"DataFrame columns: {landmarks}")
        print(f"Probability Array: {bodylang_prob}")
        print(f"Predicted Class: {bodylang_class}")
        print(f"Confidence (max probability): {max_prob:.2f}")
        print(f"Current Stage: {state['stage']}")

        # --- Updated State Logic with Forced Transition ---
        if bodylang_class == "down" and max_prob > 0.7:
            if state["stage"] != "down":
                print("Transitioning stage to 'down' (detected down)")
            state["stage"] = "down"
        elif state["stage"] == "up" and bodylang_class == "up" and max_prob < 0.80:
            print("Forcing transition to 'down' due to lower confidence in 'up'")
            state["stage"] = "down"
        elif state["stage"] == "down" and bodylang_class == "up" and max_prob > 0.7:
            print("Transitioning stage to 'up' and counting rep.")
            state["stage"] = "up"
            state["repCount"] += 1

        # Update timestamp after successful detection
        state["last_update"] = current_time

        # Log final state.
        print(f"Updated State: {state}")
        print("---------- End Debug ----------\n")
        
        state["prob"] = max_prob
        state["feedback"] = "N/A"  # You can add additional feedback based on other conditions.
        
        return state

    except Exception as e:
        print("Error in process_landmarks:", e)
        return {"error": str(e)}
