class Solution:
    def __init__(self, input):
        self.input = input

    def part_1(self) -> int:
        rules, updates = self.get_rules_and_updates(self.input)
        ordering = self.filter_updates(updates, rules, True)
        return self.get_middle_page_sum(ordering)

    def part_2(self) -> int:
        rules, updates = self.get_rules_and_updates(self.input)
        ordering = self.filter_updates(updates, rules, False)
        sorted_ordering = self.fix_ordering(ordering, rules)
        return self.get_middle_page_sum(sorted_ordering)

    def get_rules_and_updates(self, input: str) -> tuple:
        """
        Get the rules and updates from the input

        Args:
            input (str): The input to get the rules and updates from

        Returns:
            tuple: The rules and updates
        """
        rules = dict()
        updates = []
        for line in self.input.splitlines():
            if "|" in line:
                x, y = line.split("|")
                rules.setdefault(x, []).append(y)
            elif line:
                updates.append(line.split(","))
        return rules, updates

    def filter_updates(
        self, updates: list, rules: dict, expected_satisfied: bool
    ) -> list:
        """
        Filter the updates based on the rules

        Args:
            updates (list): The updates to filter
            rules (dict): The rules to filter
            expected_satisfied (bool): Whether the rule is expected to be satisfied

        Returns:
            list: The filtered updates
        """
        ordering = []
        # go through each update
        for u in range(len(updates)):
            # go through each page in the update
            is_satisfied = True
            for p in range(len(updates[u])):
                # Check if the page is in the rules
                if updates[u][p] in rules:
                    # Check if the page is satisfied
                    if not self.is_rule_satisfied(updates[u], rules, updates[u][p]):
                        is_satisfied = False
                        break
            if expected_satisfied == is_satisfied:
                ordering.append(updates[u])
        return ordering

    def is_rule_satisfied(self, update: list, rules: dict, page: str) -> bool:
        """
        Check if rule is satisfied

        Args:
            update (list): The update to check
            rules (dict): The rules to check
            page (str): The page to check

        Returns:
            bool: True if the page to move is satisfied
        """
        # Check if the page to move is alreadt satisfied
        page_index = update.index(page)
        for rule in rules[page]:
            if rule in update:
                # Check if the rule is already satisfied
                if update.index(rule) < page_index:
                    return False
        return True

    def get_middle_page_sum(self, updates: list) -> int:
        """
        Get the middle page sum

        Args:
            updates (list): The updates to get the middle page sum from

        Returns:
            int: The middle page sum
        """
        sum_pages = 0
        for update in updates:
            # Get the middle index
            middle_index = len(update) // 2
            sum_pages += int(update[middle_index])
        return sum_pages

    def fix_ordering(self, updates: list, rules: dict) -> list:
        """
        Fix the ordering of the pages in the updates
        so that the rules are satisfied

        Args:
            updates (list): The updates to fix
            rules (dict): The rules to fix

        Returns:
            list: The fixed updates
        """
        for rule in rules:
            for y in rules[rule]:
                for update in updates:
                    # Check if the rule is satisfied for this update
                    if rule in update and y in update:
                        rule_index = update.index(rule)
                        y_index = update.index(y)
                        # If rule is not satisfied (rule comes after y), swap them
                        if rule_index > y_index:
                            update.remove(rule)
                            update.insert(y_index, rule)
        return updates
