"""ID generation utilities."""

import uuid


def generate_id(prefix: str = "") -> str:
    """Generate a unique ID, optionally prefixed (e.g. 'hero_abc123')."""
    short = uuid.uuid4().hex[:8]
    return f"{prefix}_{short}" if prefix else short
