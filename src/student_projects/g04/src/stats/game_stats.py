class GameStats:
    def __init__(self, game_id, goals, cards):
        self.game_id = game_id
        self.goals = goals
        self.cards = cards

    def to_dict(self):
        return {
            "game_id": self.game_id,
            "goals": [g.to_dict() for g in self.goals],
            "cards": [c.to_dict() for c in self.cards],
        }
