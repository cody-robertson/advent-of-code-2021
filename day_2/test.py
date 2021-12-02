import pytest
from day_2.first import parse_instructions_from_input, Submarine
from day_2.second import SubmarineWithAim


def test_part_1_sample():
    instructions = parse_instructions_from_input("sample.txt")
    sub = Submarine()
    sub.follow_instructions(instructions)
    assert sub.get_product() == 150


def test_part_1_input():
    instructions = parse_instructions_from_input("input.txt")
    sub = Submarine()
    sub.follow_instructions(instructions)
    assert sub.get_product() == 1714680


def test_part_2_sample():
    instructions = parse_instructions_from_input("sample.txt")
    sub = SubmarineWithAim()
    sub.follow_instructions(instructions)
    assert sub.get_product() == 900


def test_part_2_input():
    instructions = parse_instructions_from_input("input.txt")
    sub = SubmarineWithAim()
    sub.follow_instructions(instructions)
    assert sub.get_product() == 1963088820
