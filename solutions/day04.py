class Solution:
    def __init__(self, input):
        self.input = self.convert_to_2d_array(input)

    def part_1(self, search_word="XMAS") -> int:
        wordsearch = self.input
        locations = []
        # Iterate through the wordsearch and check if the first
        # letter of the word is found at the location
        for y in range(len(wordsearch)):
            for x in range(len(wordsearch[y])):
                for found in range(self.search_for_word(wordsearch, x, y, search_word)):
                    locations.append((x, y))

        return len(locations)

    def part_2(self, search_word="MAS") -> int:
        wordsearch = self.input
        locations = []
        # Iterate through the wordsearch and check if the middle
        # letter of the word is found at the location
        for y in range(len(wordsearch)):
            for x in range(len(wordsearch[y])):
                if self.search_for_x_format(wordsearch, x, y, search_word):
                    locations.append((x, y))

        return len(locations)

    def convert_to_2d_array(self, input) -> list:
        """
        Convert the input into a 2D array

        Args:
            input (str): The input to convert

        Returns:
            list: The converted array
        """
        return [list(line) for line in input.splitlines()]

    def search_for_word(self, wordsearch_array, x, y, search_word) -> int:
        """
        Search for the word in the wordsearch

        Args:
            wordsearch_array (list): The wordsearch to search
            x (int): The x coordinate to start searching
            y (int): The y coordinate to start searching
            search_word (str): The word to search for

        Returns:
            int: The number of occurrances of the word
        """
        max_x = len(wordsearch_array[0])
        max_y = len(wordsearch_array)

        if wordsearch_array[y][x] != search_word[0]:
            return False

        # Directions to search in
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        occurrances = 0

        for dir_x, dir_y in directions:
            cur_x, cur_y = x + dir_x, y + dir_y

            found_characters = 1
            while found_characters < len(search_word):
                # Check if within bounds
                if cur_x < 0 or cur_x >= max_x or cur_y < 0 or cur_y >= max_y:
                    break

                # check if characters match
                if wordsearch_array[cur_y][cur_x] != search_word[found_characters]:
                    break

                cur_x += dir_x
                cur_y += dir_y

                found_characters += 1

            # Found the word, but it can occur in another direction
            if found_characters == len(search_word):
                occurrances += 1

        return occurrances

    def search_for_x_format(self, wordsearch_array, x, y, search_word) -> bool:
        """
        Search for the word in the wordsearch appearing in an X format - this will
        only work for 3-letter words.

        Args:
            wordsearch_array (list): The wordsearch to search
            x (int): The x coordinate to start searching
            y (int): The y coordinate to start searching
            search_word (str): The word to search for

        Returns:
            bool: True if the format is found
        """
        if len(search_word) != 3:
            raise ValueError("Only works for 3-letter words")

        middle_character = search_word[1]

        # Check if middle character matches
        if wordsearch_array[y][x] != middle_character:
            return False

        # Check if out of bounds
        if (
            x <= 0
            or y <= 0
            or x >= len(wordsearch_array[0]) - 1
            or y >= len(wordsearch_array) - 1
        ):
            return False

        # Get the corners
        corner_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        corners = [
            wordsearch_array[y + dir_y][x + dir_x] for dir_x, dir_y in corner_directions
        ]

        # Check both diagonals
        forward_diagonal = [corners[0], middle_character, corners[3]]
        backward_diagonal = [corners[1], middle_character, corners[2]]

        # Check if diagonals match
        if self.diagonal_check_helper(forward_diagonal, search_word):
            if self.diagonal_check_helper(backward_diagonal, search_word):
                return True

        return False

    def diagonal_check_helper(self, diagaonal, search_word) -> bool:
        """
        Helper function to check if the diagonal matches the search word
        in either direction

        Args:
            diagaonal (list): The diagonal to check
            search_word (str): The word to search for

        Returns:
            bool: True if the diagonal matches the search word
        """
        return diagaonal == list(search_word) or diagaonal == list(
            reversed(search_word)
        )
