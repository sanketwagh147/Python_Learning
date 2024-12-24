from dataclasses import dataclass


@dataclass
class Score:
    name: str
    score: int | None


if __name__ == "__main__":
    a_score = Score("Sanket", 100)
    b_score = Score("Sunny", 200)

    print(a_score)
    print(a_score == b_score)
