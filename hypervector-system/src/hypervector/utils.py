"""
Utility Functions

Helper functions for hypervector operations.
"""

import random
from typing import List


def generate_random_vector(dimension: int = 1024) -> List[float]:
    """
    Generate random normalized vector for testing.
    
    Args:
        dimension: Vector dimension
    
    Returns:
        Random normalized vector
    """
    vector = [random.gauss(0, 1) for _ in range(dimension)]
    
    # Normalize
    magnitude = sum(x * x for x in vector) ** 0.5
    if magnitude > 0:
        vector = [x / magnitude for x in vector]
    
    return vector


def validate_vector(vector: List[float], dimension: int) -> bool:
    """
    Validate vector dimension.
    
    Args:
        vector: Vector to validate
        dimension: Expected dimension
    
    Returns:
        True if valid
    """
    return len(vector) == dimension


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
    
    Returns:
        Cosine similarity score
    """
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have same dimension")
    
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)

