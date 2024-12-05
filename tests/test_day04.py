from utils.read_input import read_input

from solutions.day04 import Solution


def test_part_1():
    assert Solution(read_input(4, True)).part_1() == 18


def test_part_2():
    assert Solution(read_input(4, True)).part_2() == 9
