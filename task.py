import random
from utils import generate_certificate

def validate_task(task_data):
    """Validate task data (placeholder logic)."""
    # Simulate validation: 70% success rate
    return random.random() < 0.7

def complete_task(task_id, user_address, task_data):
    """Complete a task and issue a certificate if valid."""
    if validate_task(task_data):
        return generate_certificate(task_id, user_address)
    return None
