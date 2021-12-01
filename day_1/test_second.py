from day_1.first import load_input
from day_1.second import increase_count


def test_calculate_sliding_depths():
    params = load_input("sample.txt")
    result = increase_count(params)
    assert result == 5


def test_calculate_sliding_depths_real_input():
    params = load_input("input.txt")
    result = increase_count(params)
    assert result == 1518
