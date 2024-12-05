from utils.read_input import read_input

from solutions.day{{cookiecutter.__day_number}} import Solution


def test_part_1():
    assert Solution(read_input({{cookiecutter.day}}, True)).part_1() == 0


def test_part_2():
    assert Solution(read_input({{cookiecutter.day}}, True)).part_2() == 0
