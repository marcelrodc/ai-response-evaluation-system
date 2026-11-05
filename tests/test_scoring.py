def average_score(scores):
    if not scores:
        return 0.0
    return round(sum(scores.values()) / len(scores), 2)


def test_average_score():
    assert average_score({"Accuracy": 5, "Clarity": 3}) == 4.0


def test_empty_scores():
    assert average_score({}) == 0.0


def test_perfect_score():
    assert average_score({"A": 5, "B": 5, "C": 5}) == 5.0
