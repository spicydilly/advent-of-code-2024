from utils.read_input import read_input

from solutions.day01 import Solution


def test_part_1():
    assert Solution(read_input(1, True)).part_1() == 11


def test_part_2():
    assert Solution(read_input(1, True)).part_2() == 31
