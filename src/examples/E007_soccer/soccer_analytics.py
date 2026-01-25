# File: soccer_analytics.py
"""
soccer_analytics.py
Utility functions for soccer data analysis.
"""


def goal_probability(shots_on_target, goals):
    """
    Estimate scoring probability.
    shots_on_target : total shots on target
    goals : total goals scored
    """
    if shots_on_target == 0:
        return 0.0
    return goals / shots_on_target
