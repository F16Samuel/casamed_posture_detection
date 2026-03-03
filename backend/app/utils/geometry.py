import math
from typing import Tuple


def midpoint(p1: Tuple[float, float], p2: Tuple[float, float]) -> Tuple[float, float]:
    """
    Returns the midpoint between two 2D points.
    """
    return ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)


def vector(p1: Tuple[float, float], p2: Tuple[float, float]) -> Tuple[float, float]:
    """
    Returns vector from p1 to p2.
    """
    return (p2[0] - p1[0], p2[1] - p1[1])


def magnitude(v: Tuple[float, float]) -> float:
    """
    Returns magnitude (length) of a 2D vector.
    """
    return math.sqrt(v[0] ** 2 + v[1] ** 2)


def dot(v1: Tuple[float, float], v2: Tuple[float, float]) -> float:
    """
    Dot product of two 2D vectors.
    """
    return v1[0] * v2[0] + v1[1] * v2[1]


def angle_between(v1: Tuple[float, float], v2: Tuple[float, float]) -> float:
    """
    Returns angle in degrees between two 2D vectors.
    """
    mag1 = magnitude(v1)
    mag2 = magnitude(v2)

    if mag1 == 0 or mag2 == 0:
        return 0.0

    cos_theta = dot(v1, v2) / (mag1 * mag2)

    # Clamp for numerical stability
    cos_theta = max(min(cos_theta, 1.0), -1.0)

    angle_rad = math.acos(cos_theta)
    return math.degrees(angle_rad)


def vertical_reference() -> Tuple[float, float]:
    """
    Returns a unit vertical reference vector (pointing downward).
    In image coordinates, +y is downward.
    """
    return (0.0, 1.0)