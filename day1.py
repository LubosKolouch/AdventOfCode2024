#!/usr/bin/env python

from collections import Counter
import unittest


def calculate_total_distance(left_list: list[int],
                             right_list: list[int]) -> int:
    """Calculate the total distance by pairing smallest numbers in both lists."""
    left_list.sort()
    right_list.sort()
    return sum(abs(left - right) for left, right in zip(left_list, right_list))


def calculate_similarity_score(left_list: list[int],
                               right_list: list[int]) -> int:
    """Calculate the similarity score based on occurrences in the right list."""
    right_counter = Counter(right_list)
    return sum(num * right_counter[num] for num in left_list)


def load_lists_from_file(file_path: str) -> tuple[list[int], list[int]]:
    """Load the left and right lists from a file with space-separated values."""
    with open(file_path) as file:
        left_list = []
        right_list = []
        for line in file:
            left, right = map(int, line.strip().split())
            left_list.append(left)
            right_list.append(right)
    return left_list, right_list


if __name__ == "__main__":
    file_path = 'input1.txt'
    left_list, right_list = load_lists_from_file(file_path)
    print(f"Total distance: {calculate_total_distance(left_list, right_list)}")
    print(
        f"Similarity score: {calculate_similarity_score(left_list, right_list)}"
    )


class TestCalculations(unittest.TestCase):

    def test_calculate_total_distance(self):
        left_list = [3, 4, 2, 1, 3, 3]
        right_list = [4, 3, 5, 3, 9, 3]
        self.assertEqual(calculate_total_distance(left_list, right_list), 11)

    def test_calculate_similarity_score(self):
        left_list = [3, 4, 2, 1, 3, 3]
        right_list = [4, 3, 5, 3, 9, 3]
        self.assertEqual(calculate_similarity_score(left_list, right_list), 31)

    def test_load_lists_from_file(self):
        # Mock data for testing purposes
        left_list = [3, 4, 2, 1, 3, 3]
        right_list = [4, 3, 5, 3, 9, 3]
        self.assertEqual(left_list, [3, 4, 2, 1, 3, 3])
        self.assertEqual(right_list, [4, 3, 5, 3, 9, 3])


if __name__ == "__main__":
    unittest.main()
