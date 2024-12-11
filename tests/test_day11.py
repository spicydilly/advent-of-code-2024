from utils.read_input import read_input

from solutions.day11 import Solution


def test_part_1():
    assert Solution(read_input(11, True)).part_1() == 55312
