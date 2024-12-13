import numpy as np
import numpy.typing as npt
from collections import defaultdict  # learned this is valuable
from typing import Dict, Set, Tuple, List


class Solution:
    def __init__(self, input: str):
        self.input = input

    def part_1(self) -> int:
        map_array = self.convert_to_2d_array(self.input)
        regions = self.find_regions(map_array)
        total_price = self.calculate_price(map_array, regions, False)
        return total_price

    def part_2(self) -> int:
        map_array = self.convert_to_2d_array(self.input)
        regions = self.find_regions(map_array)
        total_price = self.calculate_price(map_array, regions, True)
        return total_price

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
        rows, cols = map_array.shape
        visited = {}
        regions = defaultdict(set)
        region_id = 0

        def dfs(x: int, y: int, region: str):
            """
            Perform depth-first search to identify all gardens in the region

            Args:
                x (int): The current row index
                y (int): The current column index
                region (str): The character representing the region
            """
            if (
                x < 0
                or y < 0
                or x >= rows
                or y >= cols
                or (x, y) in visited
                or map_array[x, y] != region
            ):
                return
            visited[(x, y)] = region_id
            regions[region_id].add((x, y))
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                dfs(x + dx, y + dy, region)

        for x in range(rows):
            for y in range(cols):
                if (x, y) not in visited:
                    dfs(x, y, map_array[x, y])
                    region_id += 1

        return regions

    def calculate_price(
        self,
        map_array: np.ndarray,
        regions: Dict[int, Set[Tuple[int, int]]],
        use_bulk: bool,
    ) -> int:
        """
        Calculate the total price of fencing all regions
            Default: area * perimeter
            Bulk: area * sides

        Args:
            map_array (np.ndarray): The map array
            regions (dict): A dictionary mapping region IDs to their coordinates
            use_bulk (bool): Whether to use the bulk-buy method.

        Returns:
            int: The total price of fencing all regions
        """
        rows, cols = map_array.shape
        total_price = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for region_id, gardens in regions.items():
            area = len(gardens)
            raw_edges = self.get_raw_edges(gardens, rows, cols, directions)

            if use_bulk:
                filtered_edges = self.filter_edges(raw_edges)
                total_price += area * len(filtered_edges)
            else:
                total_price += area * len(raw_edges)

        return total_price

    @staticmethod
    def get_raw_edges(
        gardens: Set[Tuple[int, int]],
        rows: int,
        cols: int,
        directions: List[Tuple[int, int]],
    ) -> Set[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Get the raw edges for a given set of gardens

        Args:
            gardens (Set[Tuple[int, int]]): The gardens in the region
            rows (int): Number of rows in the map
            cols (int): Number of columns in the map
            directions (List[Tuple[int, int]]): Possible movement directions

        Returns:
            Set[Tuple[Tuple[int, int], Tuple[int, int]]]: Set of raw edges
        """
        raw_edges = set()
        for x, y in gardens:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    nx < 0
                    or ny < 0
                    or nx >= rows
                    or ny >= cols
                    or (nx, ny) not in gardens
                ):
                    raw_edges.add(((x, y), (nx, ny)))
        return raw_edges

    @staticmethod
    def filter_edges(
        raw_edges: Set[Tuple[Tuple[int, int], Tuple[int, int]]],
    ) -> Set[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Filter edges to remove redundant internal connections

        Args:
            raw_edges (Set[Tuple[Tuple[int, int], Tuple[int, int]]]): Set of raw edges

        Returns:
            Set[Tuple[Tuple[int, int], Tuple[int, int]]]: Set of filtered edges
        """
        filtered_edges = set()
        directions = [(0, 1), (1, 0)]
        for edge1, edge2 in raw_edges:
            keep = True
            for dx, dy in directions:
                edge1_neighbor = (edge1[0] + dx, edge1[1] + dy)
                edge2_neighbor = (edge2[0] + dx, edge2[1] + dy)
                if (edge1_neighbor, edge2_neighbor) in raw_edges:
                    keep = False
            if keep:
                filtered_edges.add((edge1, edge2))
        return filtered_edges
