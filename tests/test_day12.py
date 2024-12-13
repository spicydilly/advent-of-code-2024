from utils.read_input import read_input

from solutions.day12 import Solution


def test_part_1():
    assert Solution(read_input(12, True)).part_1() == 1930


def test_part_2():
    assert Solution(read_input(12, True)).part_2() == 0
