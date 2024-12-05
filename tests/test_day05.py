from utils.read_input import read_input

from solutions.day05 import Solution


def test_part_1():
    assert Solution(read_input(5, True)).part_1() == 143


def test_part_2():
    assert Solution(read_input(5, True)).part_2() == 123
