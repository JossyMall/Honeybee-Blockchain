# utils.py

import uuid

def generate_uuid() -> str:
    """
    Generate a unique UUID
    :return: <str> UUID as string
    """
    return str(uuid.uuid4())
