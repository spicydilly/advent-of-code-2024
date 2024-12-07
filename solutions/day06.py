import numpy as np  # using this for 2d arrays
import numpy.typing as npt

from typing import Any, Optional, Tuple, Set

Location = Tuple[int, int]  # a coordinate on the map
State = Tuple[Location, str]  # a state consisting of a location and a direction


class Solution:
    # list of valid guards
    VALID_GUARDS = ["^", "v", "<", ">"]
    VALID_OBSTACLES = ["#", "O"]
    DIRECTIONS = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }
    TURN_RIGHT = {
        "^": ">",
        "v": "<",
        "<": "^",
        ">": "v",
    }

    def __init__(self, input: str):
        self.input = self.convert_to_2d_array(input)

    def part_1(self) -> int:
        map_array = self.input.copy()
        guard_location = self.find_guard_location()
        visited, _ = self.move_guard(map_array, guard_location)

        # count the unique visited locations
        return len({location for location, _ in visited})

    def part_2(self) -> int:
        map_array = self.input.copy()
        guard_location = self.find_guard_location()
        visited, _ = self.move_guard(map_array, guard_location)
        visited_locations = {location for location, _ in visited}
        loop_count = 0

        for y, x in visited_locations:
            if map_array[y, x] == ".":
                map_array[y, x] = "#"  # block the path
                _, loop = self.move_guard(map_array, guard_location, detect_loop=True)
                if loop:
                    loop_count += 1
                map_array[y, x] = "."  # restore the original

        return loop_count

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

    def move_guard(
        self,
        map_array: npt.NDArray[Any],
        guard_location: Tuple[int, int],
        detect_loop: bool = False,
    ) -> Tuple[Set[State], bool]:
        """
        Move the guard through the map

        Args:
            map_array (numpy Array): The map to move the guard on
            guard_location (tuple): The location of the guard
            detect_loop (bool): Whether to detect loops

        Returns:
            tuple: The new map and whether the guard looped
        """
        path: Set[State] = set()
        max_y, max_x = map_array.shape
        y, x = guard_location
        cur_dir = map_array[y, x].item()
        loop_detected = False

        while 0 <= y < max_y and 0 <= x < max_x:
            old_dir = cur_dir
            dir_y, dir_x = self.DIRECTIONS[cur_dir]
            new_y, new_x = y + dir_y, x + dir_x

            # Turn right when obstacle is encountered
            while (
                0 <= new_y < max_y
                and 0 <= new_x < max_x
                and map_array[new_y, new_x] in self.VALID_OBSTACLES
            ):
                cur_dir = self.TURN_RIGHT[cur_dir]
                dir_y, dir_x = self.DIRECTIONS[cur_dir]
                new_y, new_x = y + dir_y, x + dir_x

            # add current state to the path
            path.add(((y, x), old_dir))

            # check for loop
            if detect_loop and ((new_y, new_x), cur_dir) in path:
                loop_detected = True
                break

            # update the guard position
            y, x = new_y, new_x

        return path, loop_detected

    def find_guard_location(self) -> Optional[Tuple[int, int]]:
        """
        Find the location of the guard (^, v, <, >)

        Returns:
            tuple: The location of the guard
        """
        for (y, x), value in np.ndenumerate(self.input):
            if value in self.VALID_GUARDS:
                return y, x
        return None  # Guard not found
