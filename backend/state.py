# state.py
import time

class ExerciseStateWrapper:
    """
    Wrapper for the exercise state dictionary.
    If an exercise hasn’t been updated for more than reset_timeout seconds,
    its state is reinitialized on next access.
    """
    def __init__(self, reset_timeout=10):
        self._state = {}        # Internal state storage.
        self._last_reset = {}   # Timestamps for last reset per exercise.
        self._reset_timeout = reset_timeout

    def get(self, key, default=None):
        now = time.time()
        # If this exercise has never been seen or it was last reset too long ago,
        # reinitialize its state.
        if key not in self._state or (now - self._last_reset.get(key, 0)) > self._reset_timeout:
            self._state[key] = {"repCount": 0, "stage": "down", "feedback": "N/A"}
            self._last_reset[key] = now
        return self._state.get(key, default)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self._state[key] = value
        self._last_reset[key] = time.time()

    def reset_exercise(self, key):
        """
        Force a reset of the state for a given exercise.
        This can be called when a page loads.
        """
        self._state[key] = {"repCount": 0, "stage": "down", "feedback": "N/A"}
        self._last_reset[key] = time.time()

    def clear(self):
        self._state.clear()
        self._last_reset.clear()

# Global dictionary to hold real-time exercise state.
# Using our wrapper, which behaves like a normal dict for existing code.
exercise_state = ExerciseStateWrapper()
