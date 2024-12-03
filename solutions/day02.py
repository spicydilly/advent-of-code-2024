class Solution:
    def __init__(self, input):
        self.input = input

    def part_1(self):
        # No dampening
        return self.get_num_safe_reports(dampening=False)

    def part_2(self):
        # Dampening allowed
        return self.get_num_safe_reports(dampening=True)

    def get_num_safe_reports(self, dampening=False):
        # List to hold reports, False if unsafe, True if safe
        report_results = []

        # Loop each line (report)
        for report in self.input.splitlines():
            # Split the report into levels
            levels = [int(level) for level in report.split()]

            # Get the report result
            report_results.append(self.check_levels(levels, dampening=dampening))

        # return the number of safe reports
        return sum(report_results)

    def check_levels(self, levels, dampening=False):
        """
        Walk through each level in the report and make sure the integers either
        all increase or all decrease and each adjacent pair differs by at least 1
        and at most 3

        If dampening is enabled, then we can allow one one rule to be broken

        When dampening is enabled, we can remove one level from the report and recheck
        the remaining levels to see if the report is still safe

        Args:
            levels (list): List of integers
            dampening (bool, optional): Whether to dampen the check. Defaults to False.

        Returns:
            bool: True if the report is safe, False if not.
        """
        increasing = None

        for i in range(len(levels) - 1):
            # Get difference
            diff = levels[i + 1] - levels[i]

            # Check if increasing or decreasing
            if diff > 0:  # Increasing
                if increasing is False:
                    if dampening:
                        return self.dampening_helper(levels, i)
                    return False
                increasing = True
            elif diff < 0:  # Decreasing
                if increasing is True:
                    if dampening:
                        return self.dampening_helper(levels, i)
                    return False
                increasing = False

            # Check if the adjacent levels are not within 1 or 3
            if abs(diff) < 1 or abs(diff) > 3:
                if dampening:
                    return self.dampening_helper(levels, i)
                return False

        # Report is safe
        return True

    def dampening_helper(self, levels, index):
        """
        Helper function to dampen the check

        Takes in a list of levels and removes the levels around the index including
        the index and checks if the report is still safe. This helps avoid complete
        brute forcing of removing each level

        Args:
            levels (list): List of integers
            index (int): Index of the level that is unsafe

        Returns:
            bool: True if the report is safe, False if not
        """
        # Check edge cases
        indexes = [index]
        if index + 1 < len(levels):
            indexes.append(index + 1)
        if index - 1 >= 0:
            indexes.append(index - 1)

        # Remove the levels and check if the report is still safe
        for i in indexes:
            # Remove the level at i
            temp_levels = levels[:i] + levels[i + 1 :]
            if self.check_levels(temp_levels, dampening=False):
                # Report is safe with removed level
                return True

        # Report is not safe
        return False
