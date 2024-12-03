class Solution:
    def __init__(self, input):
        # first, remove newlines to make the input easier to traverse
        self.input = input.replace("\n", " ")

    def part_1(self):
        return self.mul_helper(self.check_for_commads(self.input, False))

    def part_2(self):
        return self.mul_helper(self.check_for_commads(self.input, True))

    def check_for_commads(self, commands, allow_disable=False):
        """
        Traverse the commands to find all valid mul(x,y)

        Args:
            commands (str): The commands to traverse
            allow_disable (bool, optional): Whether to allow disabling checking of mul

        Returns:
            list: A list of mul(x,y)
        """
        valid_array = []

        # Enable checking for mul
        mul_enabled = True

        # traverse the commands looking for mul(x,y)
        for i in range(len(commands)):
            # check if there is space for a mul(x,y) remaining
            if i + 8 > len(commands):
                # not enough space
                break
            if mul_enabled:
                valid_array = self.check_for_mul(commands, i, valid_array)
            if allow_disable:
                mul_enabled = self.check_for_toggles(commands, i, mul_enabled)
        return valid_array

    def check_for_mul(self, commands, i, valid_array):
        """
        Check if the commands contains mul(x,y)

        Args:
            commands (str): The commands to check
            i (int): The index of the commands to check
            valid_array (list): A list of valid mul(x,y)

        Returns:
            list: A list of valid mul(x,y)
        """
        opening_parenthesis = 0
        closing_parenthesis = 0
        if commands[i] == "m":
            # check if the next 4 characters are mul(
            if commands[i : i + 4] == "mul(":
                opening_parenthesis = i + 4
                # now find the closing parenthesis
                for j in range(opening_parenthesis, len(commands)):
                    if commands[j] == ")":
                        closing_parenthesis = j
                        break
                if closing_parenthesis != 0:
                    # now check if inside the parenthesis contains only
                    # digits and commas
                    if self.check_inner_parenthesis(
                        commands[opening_parenthesis:closing_parenthesis]
                    ):
                        valid_array.append(
                            commands[opening_parenthesis:closing_parenthesis]
                        )
                        i = closing_parenthesis

        return valid_array

    def check_inner_parenthesis(self, inner_parenthesis):
        """
        Check if the inner_parenthesis contains digits separated by a single comma

        Args:
            inner_parenthesis (str): The inner parenthesis to check

        Returns:
            bool: True if the inner_parenthesis contains digits separated by a single
                comma, False if not
        """
        # check if the inner_parenthesis contains digits separated by a single comma
        values = inner_parenthesis.split(",")
        # make sure there are 2 values
        if len(values) != 2:
            return False
        # make sure the values are digits
        for value in values:
            if not value.isdigit():
                return False
        return True

    def mul_helper(self, mul_array):
        """
        Helper function to calculate the result of all mul(x,y)

        Args:
            mul_array (list): A list of mul(x,y)

        Returns:
            int: The result of all mul(x,y)
        """
        result = 0
        for mul in mul_array:
            values = mul.split(",")
            result += int(values[0]) * int(values[1])
        return result

    def check_for_toggles(self, commands, i, current_toggle):
        """
        Check if the commands contains do() or don't()

        do() enables mul(), don't() disables mul()

        Args:
            commands (str): The commands to check
            i (int): The index of the commands to check
            current_toggle (bool): The current toggle state

        Returns:
            bool: The new toggle state"""
        # toggle on for do(), off for don't()
        if commands[i] == "d":
            if commands[i : i + 4] == "do()":
                return True
            elif commands[i : i + 7] == "don't()":
                return False

        return current_toggle
