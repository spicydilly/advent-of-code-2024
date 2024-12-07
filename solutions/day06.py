import numpy as np  # using this for 2d arrays
import numpy.typing as npt

from typing import Any, Optional


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
        # find location of the guard
        guard_location = self.find_guard_location()
        # get a copy of the map, so we can modify it
        map_copy = self.input.copy()

        # move the guard
        map_copy = self.move_guard(map_copy, guard_location)

        # return the number of visited locations
        return self.count_visited_locations(map_copy)

    def part_2(self) -> int:
        # We an ignore rows and columns that contain only '.' to
        # reduce the problem size
        new_map = self.input.copy()
        guard_location = self.find_guard_location()
        # Identify all valid locations to place an obstacle
        valid_locations = self.get_valid_obstacles_locations(new_map, guard_location)
        infinite_loop_count = 0

        for y, x in valid_locations:
            # Create a copy of the map and place an obstacle
            map_copy = new_map.copy()
            map_copy[y, x] = "O"

            # Check if the guard falls into an infinite loop
            if self.does_guard_loop(map_copy, guard_location):
                infinite_loop_count += 1
                print(f"Found infinite loop at {y}, {x}")

        return infinite_loop_count

    def convert_to_2d_array(self, input: str) -> npt.NDArray[Any]:
        """
        Convert the input into a 2D array

        Args:
            input (str): The input to convert

        Returns:
            list: The converted array
        """
        return np.array([list(line) for line in input.splitlines()])

    def move_guard(
        self, map_array: npt.NDArray[Any], guard_location: tuple[int, int]
    ) -> npt.NDArray[Any]:
        """
        Move the guard through the map

        Args:
            map_array (numpy Array): The map to move the guard on
            guard_location (tuple): The location of the guard

        Returns:
            numpy Array: The map with the path of the guard
        """
        # move the guard in the direction it's facing
        while guard_location is not None:
            movement = self.move_guard_in_direction(map_array, guard_location)
            # mark the location of the guard as visited
            map_array[guard_location] = "X"
            # update the location of the guard
            if movement is None:
                break
            guard_location = movement[0]
            # update the map with the guards direction
            map_array[guard_location] = movement[1]

        return map_array

    def find_guard_location(self) -> Optional[tuple[int, int]]:
        """
        Find the location of the guard (^, v, <, >)

        Returns:
            tuple: The location of the guard
        """
        for (y, x), value in np.ndenumerate(self.input):
            if value in self.VALID_GUARDS:
                return y, x
        return None  # Guard not found

    def move_guard_in_direction(
        self, map_array: npt.NDArray[Any], guard_location: tuple[int, int]
    ) -> Optional[tuple[tuple[int, int], str, bool]]:
        """
        Move the guard in the direction it's facing

        Args:
            map_array (numpy Array): The map to move the guard on
            guard_location (tuple): The location of the guard

        Returns:
            tuple: The new location of the guard, and the direction it's facing
        """
        # convert the guard location to integers
        y, x = guard_location
        guard_symbol = map_array[y, x].item()

        # check if the guard is valid
        if guard_symbol not in self.VALID_GUARDS:
            raise ValueError(f"Invalid guard symbol: {guard_symbol}")

        # check what is in front of the guard
        in_front = self.check_in_direction(map_array, guard_location, guard_symbol)

        # check if we are not out of bounds
        if in_front is None:
            return None

        if in_front in [".", "X"]:
            dy, dx = self.DIRECTIONS[guard_symbol]
            return (y + dy, x + dx), guard_symbol, False
        elif in_front in self.VALID_OBSTACLES:  # turn right 90 degrees
            guard_symbol = self.turn_right(guard_symbol)
            return guard_location, guard_symbol, True

        return None

    def check_in_direction(
        self,
        map_array: npt.NDArray[Any],
        guard_location: tuple[int, int],
        guard_symbol: str,
    ) -> Optional[str]:
        """
        Check what is in front of the guard
            ^ - up
            v - down
            < - left
            > - right

        Args:
            map_array (numpy Array): The map to check
            guard_location (tuple): The location of the guard
            guard_symbol (str): The symbol of the guard

        Returns:
            str: The symbol in front of the guard
        """
        y, x = guard_location
        dy, dx = self.DIRECTIONS[guard_symbol]
        try:
            return map_array[y + dy, x + dx].item()
        except IndexError:
            # guard is now out of bounds
            return None

    def turn_right(self, guard_symbol: str) -> str:
        """
        Turn the guard right

        Args:
            guard_symbol (str): The symbol of the guard

        Returns:
            str: The new symbol of the guard
        """
        return self.TURN_RIGHT[guard_symbol]

    def count_visited_locations(self, map_array: npt.NDArray[Any]) -> int:
        """
        Count the number of visited locations

        Args:
            map_array (numpy Array): The map to count the visited locations on

        Returns:
            int: The number of visited locations
        """
        return np.count_nonzero(map_array == "X")

    def get_valid_obstacles_locations(
        self, map_array: npt.NDArray[Any], start_location: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """
        Get the valid obstacle locations

        Args:
            map_array (numpy Array): The map to get the valid obstacle locations from
            start_location (tuple): The start location of the guard

        Returns:
            list: The valid obstacle locations
        """
        map_copy = map_array.copy()
        # valid locations are places that are visited in part one!
        guard_location = self.find_guard_location()
        map_with_visits = self.move_guard(map_copy, guard_location)
        # remove the start location
        map_with_visits[start_location] = "."
        return np.argwhere(map_with_visits == "X")

    def does_guard_loop(
        self, map_array: npt.NDArray[Any], guard_location: tuple[int, int]
    ) -> bool:
        visited_states = set()
        map_copy = map_array.copy()

        # Initial direction of the guard
        guard_symbol = map_copy[guard_location].item()
        # visited_states.add((guard_location, guard_symbol))

        while True:
            prev_state = (guard_location, guard_symbol)
            movement = self.move_guard_in_direction(map_copy, guard_location)
            if movement is None:
                # No further movement means no loop
                return False
            new_guard_location, new_guard_symbol, changed_direction = movement

            if changed_direction:
                # Check if we've seen this exact state (position + direction) before
                # from the same direction
                new_state = prev_state
                # print(new_state)
                if new_state in visited_states:
                    return True  # Found a loop
                visited_states.add(new_state)

            # Update the map and guard position
            map_copy[guard_location] = "X"
            guard_location, guard_symbol = new_guard_location, new_guard_symbol
            map_copy[guard_location] = guard_symbol
