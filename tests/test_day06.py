from utils.read_input import read_input

from solutions.day06 import Solution


def test_part_1():
    assert Solution(read_input(6, True)).part_1() == 41


def test_part_2():
    assert Solution(read_input(6, True)).part_2() == 6
