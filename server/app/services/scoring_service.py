import numpy as np
from typing import Dict


def score_low_is_better(value: float, min_val: float, max_val: float) -> float:
    """
    Lower values get higher scores (e.g., cloud cover for stargazing).
    Returns a score from 0-100.

    Args:
        value: The parameter value to score
        min_val: Minimum possible value for normalization
        max_val: Maximum possible value for normalization

    Returns:
        Score from 0-100, where lower input values get higher scores
    """
    if max_val == min_val:
        return 100.0

    normalized = (value - min_val) / (max_val - min_val)
    normalized = np.clip(normalized, 0, 1)
    return (1 - normalized) * 100


def score_high_is_better(value: float, min_val: float, max_val: float) -> float:
    """
    Higher values get higher scores (e.g., sunshine for beach days).
    Returns a score from 0-100.

    Args:
        value: The parameter value to score
        min_val: Minimum possible value for normalization
        max_val: Maximum possible value for normalization

    Returns:
        Score from 0-100, where higher input values get higher scores
    """
    if max_val == min_val:
        return 100.0

    normalized = (value - min_val) / (max_val - min_val)
    normalized = np.clip(normalized, 0, 1)
    return normalized * 100


def score_optimal_range(
    value: float,
    optimal_min: float,
    optimal_max: float,
    falloff_rate: float = 2.0
) -> float:
    """
    Values within the optimal range get score 100.
    Values outside fall off gradually based on falloff_rate.
    Uses trapezoidal function for smooth scoring.

    Args:
        value: The parameter value to score
        optimal_min: Lower bound of optimal range
        optimal_max: Upper bound of optimal range
        falloff_rate: How quickly score decreases outside range (higher = faster falloff)

    Returns:
        Score from 0-100, with 100 for values in optimal range
    """
    if optimal_min <= value <= optimal_max:
        return 100.0

    # Calculate distance from optimal range
    if value < optimal_min:
        distance = optimal_min - value
        range_width = optimal_max - optimal_min
    else:  # value > optimal_max
        distance = value - optimal_max
        range_width = optimal_max - optimal_min

    # Apply exponential falloff
    score = 100 * np.exp(-(distance / (range_width * falloff_rate)) ** 2)
    return max(0.0, score)


def calculate_weighted_score(
    parameter_scores: Dict[str, float],
    weights: Dict[str, float]
) -> float:
    """
    Calculates the weighted average of parameter scores.

    Args:
        parameter_scores: Dictionary mapping parameter IDs to their scores
        weights: Dictionary mapping parameter IDs to their weights

    Returns:
        Weighted average score from 0-100
    """
    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0.0

    weighted_sum = sum(
        parameter_scores.get(param_id, 0) * weight
        for param_id, weight in weights.items()
    )

    return weighted_sum / total_weight
