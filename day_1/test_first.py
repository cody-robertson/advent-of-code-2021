from day_1.first import load_input, increase_count


def test_calculate_depths():
    params = load_input("part_1_input_1.txt")
    result = increase_count(params)
    assert result == 7
