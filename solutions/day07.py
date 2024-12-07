from typing import List, Tuple
from itertools import product


class Solution:

    def __init__(self, input: str):
        self.input = input

    def part_1(self) -> int:
        operators = "+*"
        expression = self.get_calibrations(self.input)
        return self.begin_calculations(expression, operators)

    def part_2(self) -> int:
        # the problem calls for ||, but for simplicity I'm using |
        operators = "+*|"
        expression = self.get_calibrations(self.input)
        return self.begin_calculations(expression, operators)

    def get_calibrations(self, input: str) -> List[Tuple[str, List[int]]]:
        """
        Get the calibrations from the input

        Args:
            input (str): The input to get the calibrations from

        Returns:
            List[Tuple[str, List[int]]]: The calibrations
        """
        calibrations = []
        for line in self.input.splitlines():
            temp_values = line.split()
            test_value = int(temp_values[0][:-1])
            numbers = list(map(int, temp_values[1:]))
            calibrations.append((test_value, numbers))
        return calibrations

    def begin_calculations(
        self, expression: List[Tuple[int, List[int]]], operators: str
    ) -> int:
        """
        Calculate the sum of valid calibrations

        Args:
            expression (List[Tuple[int, List[int]]]): The calibrations to evaluate
            operators (str): The operators to evaluate

        Returns:
            int: The sum of valid calibrations
        """
        total = 0
        for target, numbers in expression:
            # Generate operator combinations
            n = len(numbers)
            valid_operators = product(operators, repeat=n - 1)

            for operator_combo in valid_operators:
                # Evaluate the current combination
                if self.is_valid_combination(numbers, operator_combo, target):
                    total += target
                    break  # Stop after finding the first valid combination
        return total

    def is_valid_combination(
        self, numbers: List[int], operators: Tuple[str], target: int
    ) -> bool:
        """
        Check if the combination of numbers and operators is valid

        Args:
            numbers (List[int]): The numbers to evaluate
            operators (Tuple[str]): The operators to evaluate
            target (int): The target to evaluate

        Returns:
            bool: True if the combination is valid
        """
        result = numbers[0]
        for i, operator in enumerate(operators):
            if operator == "+":
                result += numbers[i + 1]
            elif operator == "*":
                result *= numbers[i + 1]
            elif operator == "|":
                # Concatenate as strings and convert back to int
                result = int(str(result) + str(numbers[i + 1]))

            # Check if the result is greater than the target
            # If it is, the combination is never valid
            # as we cannot decrease the result
            # This only works becase the operators are additive
            if int(result) > target:
                return False

        return result == target
