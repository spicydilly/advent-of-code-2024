import numpy as np  # using this for 2d arrays
import numpy.typing as npt

from typing import Any, List, Dict, Tuple, Set
from itertools import combinations


class Solution:
    def __init__(self, input: str):
        self.input = self.convert_to_2d_array(input)

    def part_1(self) -> int:
        unique_antennas = self.get_unqiue_antennas(self.input)
        pairs_of_antennas = self.get_pairs(self.input, unique_antennas)
        antinodes, _ = self.find_antinodes(self.input, pairs_of_antennas, False)
        return len(antinodes)

    def part_2(self) -> int:
        unique_antennas = self.get_unqiue_antennas(self.input)
        pairs_of_antennas = self.get_pairs(self.input, unique_antennas)
        _, antinodes_harmonics = self.find_antinodes(
            self.input, pairs_of_antennas, True
        )
        return len(antinodes_harmonics)

    @staticmethod
    def convert_to_2d_array(input: str) -> npt.NDArray[Any]:
        """
        Convert the input into a 2D array

        Args:
            input (str): The input to convert

        Returns:
            list: The converted array
        """
        return np.array([list(line) for line in input.splitlines()])

    @staticmethod
    def get_unqiue_antennas(map_array: npt.NDArray[Any]) -> List[str]:
        """
        Get the unique antennas in the map

        Args:
            map_array (npt.NDArray[Any]): The map to get the antennas from

        Returns:
            List[str]: The unique antennas
        """
        return list(set(map_array[map_array != "."]))

    @staticmethod
    def get_pairs(
        map_array: npt.NDArray[Any], unique_antennas: List[str]
    ) -> Dict[str, List[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        """
        Get the pairs of antennas in the map for each frequency

        Args:
            map_array (npt.NDArray[Any]): The map to get the pairs from
            unique_antennas (List[str]): The unique antennas

        Returns:
            dict: A dictionary of frequencies, with a list of pairs of antennas
        """
        result = {}

        for antenna in unique_antennas:
            positions = list(zip(*np.where(map_array == antenna)))
            if len(positions) > 1:
                result[antenna] = list(combinations(positions, 2))

        return result

    def find_antinodes(
        self,
        map_array: npt.NDArray[Any],
        antennas: Dict[str, Tuple[int, int]],
        resonant_harmonics: bool = False,
    ) -> Tuple[Set[Tuple[int, int]], Set[Tuple[int, int]]]:
        """
        Find the antinodes in the map, every pair of antennas has two antinodes

        Args:
            map_array (npt.NDArray[Any]): The map to find the antinodes in
            antennas (Dict[str, Tuple[int, int]]): The antennas to find the
                antinodes for

        Returns:
            tuple: The antinodes and the antinodes for resonant harmonics
        """
        x, y = map_array.shape
        antinodes = set()
        antinodes_harmonics = set()

        for frequency, antenna_pairs in antennas.items():
            for pair in antenna_pairs:
                (x1, y1), (x2, y2) = pair
                # get vector between the antennas
                vx = x2 - x1
                vy = y2 - y1

                # check if the antinodes are in bounds
                # antinodes are placed at extensions of the deltas
                if self.is_inbounds(x1 - vx, y1 - vy, x, y):
                    antinodes.add((x1 - vx, y1 - vy))
                if self.is_inbounds(x2 + vx, y2 + vy, x, y):
                    antinodes.add((x2 + vx, y2 + vy))

                if resonant_harmonics:
                    antinodes_harmonics.update(
                        self.get_collinear_points(x1, y1, vx, vy, x, y)
                    )

        return antinodes, antinodes_harmonics

    @staticmethod
    def is_inbounds(x: int, y: int, x_max: int, y_max: int) -> bool:
        """
        Check if the given coordinates are in bounds

        Args:
            x (int): The x coordinate
            y (int): The y coordinate
            x_max (int): The maximum x value
            y_max (int): The maximum y value

        Returns:
            bool: True if the coordinates are in bounds, False otherwise
        """
        return 0 <= x < x_max and 0 <= y < y_max

    def get_collinear_points(
        self, x: int, y: int, vx: int, vy: int, rows: int, cols: int
    ) -> Set[Tuple[int, int]]:
        """
        Get all collinear points along the vector in both directions

        Args:
            x (int): Starting x-coordinate
            y (int): Starting y-coordinate
            vx (int): Vector x (step along x-axis)
            vy (int): Vector y (step along y-axis)
            rows (int): Number of rows in the grid
            cols (int): Number of columns in the grid

        Returns:
            Set[Tuple[int, int]]: A set of all collinear points within bounds
        """
        points = set()
        points.add((x, y))
        # Traverse in the forward direction
        cur_x, cur_y = x, y
        while True:
            cur_x += vx
            cur_y += vy
            if not self.is_inbounds(cur_x, cur_y, rows, cols):
                break
            points.add((cur_x, cur_y))

        # Traverse in the backward direction
        cur_x, cur_y = x, y
        while True:
            cur_x -= vx
            cur_y -= vy
            if not self.is_inbounds(cur_x, cur_y, rows, cols):
                break
            points.add((cur_x, cur_y))

        return points
