"""
Implements Scoreboard Class
"""

from dataclasses import dataclass, field


@dataclass
class Score:
    name: str
    score: int


@dataclass
class Position:
    position: int
    score: int | None = None
    users: list[str] = field(default_factory=list)


# TODO: Later
class Scorecard:
    """

    Methods:
    1. to_scores
    2. set_top_score(Score)
    3. get nth top score()
    3. _check_if_top_score(Score.value)

    """

    def __init__(self, top_n=10) -> None:
        self._capacity = top_n
        self._top_scores: list[Position] = [
            Position(
                position=i + 1,
            )
            for i in range(top_n)
        ]
        self._num_of_curr_scores = 0

    def nth_top(self, n: int):
        try:
            nth_score = self._top_scores[n - 1]
            if nth_score is None:
                return f"{n}: spot is empty"
        except IndexError as err:
            raise IndexError("Score does not exist") from err

    def print_top_scores(self):
        for each in self._top_scores:
            print(each)

    @property
    def top_scores(self):
        return self._top_scores

    def add_score(self, score: Score):
        if self._num_of_curr_scores < self._capacity:
            if self._num_of_curr_scores == 0:
                current_position = self._num_of_curr_scores + 1
                position = Position(
                    score=score.score, users=[score.name], position=current_position
                )
                self._top_scores[self._num_of_curr_scores] = position
                self._num_of_curr_scores += 1
                return True
            else:
                for i in range(len(self._top_scores)):
                    if (
                        self._top_scores[i].score is not None
                        and self._top_scores[i].score < score.score  # type: ignore
                    ):
                        self._top_scores[i].score = score.score
                        self._top_scores[i].users = [score.name]
                        current_position = self._num_of_curr_scores + 1
                        self._num_of_curr_scores += 1
                        return True
                    if (
                        self._top_scores[i].score is not None
                        and self._top_scores[i].score == score.score
                    ):
                        self._top_scores[i].users.append(score.name)
                        return True
        # assume last score is lowest
        # check if this is greater than other scores:

    def insert_high_score(self): ...


if __name__ == "__main__":

    road_rash = Scorecard(5)
    sanket = Score("Sanket", 100)
    user1 = Score("user1", 90)
    user2 = Score("user2", 80)
    user3 = Score("user3", 70)
    user4 = Score("user4", 60)
    user5 = Score("user5", 50)
    road_rash.add_score(sanket)
    road_rash.add_score(user1)
    # road_rash.add_score(user2)
    # road_rash.add_score(user3)
    # road_rash.add_score(user4)

    road_rash.print_top_scores()
