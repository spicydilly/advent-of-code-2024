from utils.read_input import read_input

from solutions.day10 import Solution


def test_part_1():
    assert Solution(read_input(10, True)).part_1() == 36


def test_part_2():
    assert Solution(read_input(10, True)).part_2() == 81
