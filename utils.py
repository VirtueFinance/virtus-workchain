import hashlib
import json

def sha256_hash(data):
    """Compute SHA-256 hash of the input data."""
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def generate_certificate(task_id, user_address):
    """Generate a simple certificate for task completion."""
    timestamp = time.time()
    signature = hashlib.sha256(f"{task_id}{user_address}{timestamp}".encode()).hexdigest()
    return {
        "task_id": task_id,
        "user_address": user_address,
        "timestamp": timestamp,
        "signature": signature
    }
