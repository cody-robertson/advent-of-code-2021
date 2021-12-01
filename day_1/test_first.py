from day_1.first import load_input, increase_count


def test_calculate_depths():
    params = load_input("sample.txt")
    result = increase_count(params)
    assert result == 7


def test_calculate_depths_real_input():
    params = load_input("input.txt")
    result = increase_count(params)
    assert result == 1482
