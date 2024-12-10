from utils.read_input import read_input

from solutions.day08 import Solution


def test_part_1():
    assert Solution(read_input(8, True)).part_1() == 14


def test_part_2():
    assert Solution(read_input(8, True)).part_2() == 34
