from typing import List


class Solution:
    def __init__(self, input: str):
        self.input = [int(x) for x in input.strip().split(" ")]

    def part_1(self) -> int:
        number_of_blinks = 25
        stones_after_blinks = self.transform_stones(self.input, number_of_blinks)
        return len(stones_after_blinks)

    def part_2(self) -> int:
        # Implement Part 2 logic
        pass

    @staticmethod
    def transform_stones(stones: List[int], blinks: int) -> List[int]:
        """
        Transform the stones, for x blinks following the rules in order:
            1. If stone is 0, replace with 1
            2. If stone is even number of digits, replace with 2 stones. Left half of
                digits is first stone, right half is second stone
                (remove leading zeros)
            3. If no rules apply, replace with new stone with value multiplying by 2024

        Args:
            stones (List[int]): The stones to transform
            blinks (int): The number of blinks

        Returns:
            List[str]: The transformed stones
        """
        new_stones = stones.copy()
        # Implement the transformation logic
        for _ in range(blinks):
            new_stones = []
            for stone in stones:
                if stone == 0:
                    # Rule 1: Replace 0 with 1
                    new_stones.append(1)
                elif len(str(stone)) % 2 == 0:
                    # Rule 2: Split even-digit stones into two stones
                    str_stone = str(stone)
                    mid = len(str_stone) // 2
                    left, right = str_stone[:mid], str_stone[mid:]
                    new_stones.append(
                        int(left.lstrip("0") or "0")
                    )  # Avoid empty strings
                    new_stones.append(
                        int(right.lstrip("0") or "0")
                    )  # Avoid empty strings
                else:
                    # Rule 3: Multiply by 2024
                    new_stones.append(stone * 2024)
            stones = new_stones  # Update stones for the next blink
        return stones
