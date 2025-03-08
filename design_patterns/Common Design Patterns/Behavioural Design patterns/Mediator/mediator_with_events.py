"""
Mediator with events
"""

from typing import Any


class Event(list):

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        for item in self:
            item(*args, **kwds)


class Game:
    """
    This is a mediator
    """

    def __init__(self) -> None:
        self.events = Event()

    def fire(self, args):
        self.events(args)


class GoalScoredInfo:
    def __init__(self, who_scored, goals_scored) -> None:
        self.who_scored = who_scored
        self.goals_scored = goals_scored


class Player:
    def __init__(self, name, game) -> None:
        self.name = name
        self.game = game
        self.goal_scored = 0

    def score(self):
        self.goal_scored += 1
        args = GoalScoredInfo(self.name, self.goal_scored)
        self.game.fire(args)


class Coach:
    def __init__(self, game) -> None:
        game.events.append(self.celebrate_goals)

    def celebrate_goals(self, args):
        if isinstance(args, GoalScoredInfo) and args.goals_scored < 4:
            print(f"Coach congratulates {args.who_scored}")


if __name__ == "__main__":
    game = Game()
    san = Player("san", game)
    coach = Coach(game)
    san.score()
    san.score()
    san.score()
