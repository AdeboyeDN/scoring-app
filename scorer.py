import time
import random

class Scorer:
    def __init__(self):
        # Load your model here (e.g., sklearn, torch)
        pass

    def score(self, features: dict) -> float:
        # Simulate model prediction latency
        time.sleep(1)
        # Return a mock score
        return round(random.uniform(0, 1), 4)
