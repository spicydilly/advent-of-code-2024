from utils.read_input import read_input

from solutions.day09 import Solution


def test_part_1():
    assert Solution(read_input(9, True)).part_1() == 1928


def test_part_2():
    assert Solution(read_input(9, True)).part_2() == 2858
