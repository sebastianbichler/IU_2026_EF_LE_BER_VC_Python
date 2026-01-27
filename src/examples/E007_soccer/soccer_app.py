# File: soccer_app.py
from soccer_analytics import goal_probability

p = goal_probability(shots_on_target=20, goals=5)
print("Estimated probability :", p)
