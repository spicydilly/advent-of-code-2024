from utils.read_input import read_input

from solutions.day02 import Solution


def test_part_1():
    assert Solution(read_input(2, True)).part_1() == 2


def test_part_2():
    assert Solution(read_input(2, True)).part_2() == 4
