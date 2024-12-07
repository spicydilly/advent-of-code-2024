from utils.read_input import read_input

from solutions.day07 import Solution


def test_part_1():
    assert Solution(read_input(7, True)).part_1() == 3749


def test_part_2():
    assert Solution(read_input(7, True)).part_2() == 11387
