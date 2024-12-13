import numpy as np
import numpy.typing as npt
from collections import defaultdict  # learned this is valuable
from typing import Dict, Set, Tuple


class Solution:
    def __init__(self, input: str):
        self.input = input

    def part_1(self) -> int:
        map_array = self.convert_to_2d_array(self.input)
        print(map_array)
        regions = self.find_regions(map_array)
        total_price = self.calculate_total_price(map_array, regions)
        return total_price

    def part_2(self) -> int:
        # Implement Part 2 logic
        pass

    @staticmethod
    def convert_to_2d_array(input: str) -> npt.NDArray[str]:
        """
        Convert the input into a 2D array

        Args:
            input (str): The input to convert

        Returns:
            list: The converted array
        """
        return np.array([list(line) for line in input.splitlines()])

    def find_regions(
        self, map_array: npt.NDArray[str]
    ) -> Dict[int, Set[Tuple[int, int]]]:
        """
        Find the regions in the map

        Args:
            map_array (npt.NDArray[str]): The map to find the regions in

        Returns:
            dict: A dictionary of regions IDs, with a set of coordinates
        """
        max_x, max_y = map_array.shape
        visited = {}
        regions = defaultdict(set)
        region_id = 0

        def dfs(x: int, y: int, region: str):
            """
            Perform depth-first search to identify all gardens in the region

            Args:
                x (int): The current row index.
                y (int): The current column index.
                region (str): The character representing the region.
            """
            if (
                x < 0
                or y < 0
                or x >= max_x
                or y >= max_y
                or (x, y) in visited
                or map_array[x, y] != region
            ):
                return
            visited[(x, y)] = region_id
            regions[region_id].add((x, y))
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                dfs(x + dx, y + dy, region)

        for x in range(max_x):
            for y in range(max_y):
                if (x, y) not in visited:
                    dfs(x, y, map_array[x, y])
                    region_id += 1

        return regions

    def calculate_total_price(
        self, map_array: np.ndarray, regions: Dict[int, Set[Tuple[int, int]]]
    ) -> int:
        """
        Calculate the total price of fencing all regions

        Args:
            map_array (np.ndarray): The map array
            regions (dict): A dictionary mapping region IDs to their coordinates

        Returns:
            int: The total price of fencing all regions
        """
        max_x, max_y = map_array.shape
        total_price = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for region_id, cells in regions.items():
            area = len(cells)
            perimeter = 0

            for x, y in cells:
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if (
                        nx < 0
                        or ny < 0
                        or nx >= max_x
                        or ny >= max_y
                        or (nx, ny) not in cells
                    ):
                        perimeter += 1

            total_price += area * perimeter

        return total_price
