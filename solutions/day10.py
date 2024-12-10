import numpy as np
import numpy.typing as npt

from typing import Set, Tuple, List


class Solution:
    def __init__(self, input: str):
        self.input = self.convert_to_2d_array(input)

    def part_1(self) -> int:
        hiking_map = self.input
        trailheads = self.find_trailheads(hiking_map)

        return sum(
            len(self.find_hiking_paths(hiking_map, trailhead[0], trailhead[1], set()))
            for trailhead in trailheads
        )

    def part_2(self) -> int:
        hiking_map = self.input
        trailheads = self.find_trailheads(hiking_map)

        total_paths = 0
        for trailhead in trailheads:
            reachable = self.find_hiking_paths(
                hiking_map, trailhead[0], trailhead[1], set()
            )
            total_paths += sum(
                self.find_number_of_possible_paths(hiking_map, trailhead, destination)
                for destination in reachable
            )
        return total_paths

    @staticmethod
    def convert_to_2d_array(input: str) -> npt.NDArray[int]:
        """
        Convert the input into a 2D array

        Args:
            input (str): The input to convert

        Returns:
            list: The converted array
        """
        return np.array([list(map(int, line)) for line in input.splitlines()])

    @staticmethod
    def find_trailheads(hiking_map: npt.NDArray[int]) -> Set[Tuple[int, int]]:
        """
        Find the trailheads in the hiking map

        Args:
            hiking_map (npt.NDArray[int]): The hiking map to find the trailheads in

        Returns:
            Set[Tuple[int, int]]: The trailheads locations
        """
        # find the x and y coordinates of the trailheads
        x, y = np.where(hiking_map == 0)
        return set(zip(x, y))

    @staticmethod
    def find_hiking_paths(
        hiking_map: npt.NDArray[int], x: int, y: int, visited: Set[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """
        Find the hiking paths in the hiking map from the trailheads
            to values of 9. A path must increase by 1 each step.

        Args:
            hiking_map (npt.NDArray[int]): The hiking map to find the hiking paths in
            x (int): The x coordinate of the trailhead
            y (int): The y coordinate of the trailhead
            visited (Set[Tuple[int, int]]): The visited locations

        Returns:
            int: The number of 9s reachable from the trailhead
        """
        max_y, max_x = hiking_map.shape
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
        stack = [(x, y)]
        reachable = []

        # use a depth-first search to find the hiking paths
        while stack:
            px, py = stack.pop()
            if (px, py) in visited:
                continue
            visited.add((px, py))

            # check if destination reached
            if hiking_map[px, py] == 9:
                reachable.append((px, py))
                continue

            # check each direction
            for dx, dy in directions:
                new_x, new_y = px + dx, py + dy

                if (
                    0 <= new_x < max_x
                    and 0 <= new_y < max_y
                    and (new_x, new_y) not in visited
                    and hiking_map[new_x, new_y] == hiking_map[px, py] + 1
                ):
                    # add the new location to the stack
                    stack.append((new_x, new_y))

        return reachable

    @staticmethod
    def find_number_of_possible_paths(
        hiking_map: npt.NDArray[int],
        trailhead: Tuple[int, int],
        destination: Tuple[int, int],
    ) -> int:
        """
        Find the number of possible paths from the trailhead to the destination, still
            following the rules about increasing by 1

        Args:
            hiking_map (npt.NDArray[int]): The hiking map
            trailhead (Tuple[int, int]): The trailhead
            destination (Tuple[int, int]): The destination

        Returns:
            int: The number of possible paths
        """
        max_y, max_x = hiking_map.shape
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
        memory = {}

        def dfs(x: int, y: int) -> int:
            """
            Perform a depth-first search of the hiking map, starting at location (x, y)

            Args:
                x (int): The x coordinate of the location
                y (int): The y coordinate of the location

            Returns:
                int: The number of possible paths from the location to the destination
            """
            if (x, y) == destination:
                return 1

            if (x, y) in memory:
                return memory[(x, y)]

            path_count = 0
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy

                if (
                    0 <= new_x < max_y
                    and 0 <= new_y < max_x
                    and hiking_map[new_x, new_y] == hiking_map[x, y] + 1
                ):
                    path_count += dfs(new_x, new_y)

            memory[(x, y)] = path_count
            return path_count

        return dfs(trailhead[0], trailhead[1])
