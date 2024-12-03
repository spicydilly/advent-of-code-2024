from utils.read_input import read_input

from solutions.day03 import Solution


def test_part_1():
    assert Solution(read_input(3, True, 1)).part_1() == 161


def test_part_2():
    assert Solution(read_input(3, True, 2)).part_2() == 48
