class PlayerStats:
    def __init__(self, player_id, game_id, competition_id, cards, goals):
        self.player_id = player_id
        self.game_id = game_id
        self.competition_id = competition_id
        self.cards = cards
        self.goals = goals

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "game_id": self.game_id,
            "competition_id": self.competition_id,
            "cards": [c.to_dict() for c in self.cards],
            "goals": [g.to_dict() for g in self.goals],
        }
