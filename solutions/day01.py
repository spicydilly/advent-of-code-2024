class Solution:
    def __init__(self, input):
        self.input = input

    def part_1(self):
        left, right = self.separate_lists(self.input)

        # Sort each list
        sorted_left = sorted(left)
        sorted_right = sorted(right)

        # Find how far apart each number in the lists are, and sum them up
        # abs(x - y) returns the absolute value
        return sum([abs(sorted_left[i] - sorted_right[i]) for i in range(len(left))])

    def part_2(self):
        left, right = self.separate_lists(self.input)

        # Loop left list, and find number of occurences in right list and multiply them
        similarity = []
        for i in left:
            if i in right:
                # Count number of occurences
                similarity.append(i * right.count(i))

        # Sum the number of occurences to get similarity score
        return sum(similarity)

    def separate_lists(self, lists):
        # Split the input into two lists, left and right
        left = []
        right = []
        for line in self.input.splitlines():
            a, b = map(int, line.split())
            left.append(a)
            right.append(b)
        return left, right
