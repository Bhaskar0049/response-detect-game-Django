"""
Utility functions for the game application.

These helpers encapsulate logic that is shared across the app, such
as calculating the final score based on hits, combos and remaining time.
"""

def compute_score(hits: int, combos: int, time_left: float) -> int:
    """Compute the final score based on game metrics.

    :param hits: Number of targets successfully hit by the player.
    :param combos: Number of combo bonuses achieved (consecutive hits within a small time window).
    :param time_left: Remaining seconds when the game ended.
    :returns: The calculated score as an integer.

    Scoring formula:
    * Each hit yields 10 points.
    * Each combo yields 5 additional points.
    * Remaining time contributes 1 point per whole second left.
    """
    return hits * 10 + combos * 5 + int(time_left)