class TeamStats:
    def __init__(
        self,
        team_id,
        competition_id,
        wins,
        draws,
        losses,
        goals_for,
        goals_against
    ):
        self.team_id = team_id
        self.competition_id = competition_id
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.goals_for = goals_for
        self.goals_against = goals_against

    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against

    @property
    def points(self):
        return self.wins * 3 + self.draws

    def to_dict(self):
        return {
            "team_id": self.team_id,
            "competition_id": self.competition_id,
            "wins": self.wins,
            "draws": self.draws,
            "losses": self.losses,
            "goals_for": self.goals_for,
            "goals_against": self.goals_against,
            "goal_difference": self.goal_difference,
            "points": self.points,
        }
