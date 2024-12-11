from typing import List
from collections import Counter


class Solution:
    def __init__(self, input: str):
        self.input = [int(x) for x in input.strip().split(" ")]

    def part_1(self) -> int:
        number_of_blinks = 25
        stones_after_blinks = self.transform_stones(self.input, number_of_blinks)
        return stones_after_blinks

    def part_2(self) -> int:
        number_of_blinks = 75
        stones_after_blinks = self.transform_stones(self.input, number_of_blinks)
        return stones_after_blinks

    @staticmethod
    def transform_stones(stones: List[int], blinks: int) -> int:
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
            int: The total number of stones
        """

        def transform(stone: int) -> List[int]:
            """Transform a single stone using the rules."""
            if stone == 0:
                return [1]
            elif len(str(stone)) % 2 == 0:
                str_stone = str(stone)
                mid = len(str_stone) // 2
                left = int(str_stone[:mid].lstrip("0") or "0")
                right = int(str_stone[mid:].lstrip("0") or "0")
                return [left, right]
            else:
                return [stone * 2024]

        # Use a Counter to track the frequency of each stone
        stone_counts = Counter(stones)

        for _ in range(blinks):
            new_stone_counts = Counter()
            for stone, count in stone_counts.items():
                transformed = transform(stone)
                for new_stone in transformed:
                    new_stone_counts[new_stone] += count
            stone_counts = new_stone_counts  # Update for the next blink

        # get the total number of stones
        result = 0
        for count in stone_counts.values():
            result += count

        return result
