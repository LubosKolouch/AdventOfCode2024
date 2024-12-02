#!/usr/bin/env python

import unittest


def is_increasing_or_decreasing(row):
    return all(row[i] < row[i + 1] for i in range(len(row) - 1)) or \
           all(row[i] > row[i + 1] for i in range(len(row) - 1))


def has_valid_differences(row):
    return all(1 <= abs(row[i] - row[i + 1]) <= 3 for i in range(len(row) - 1))


def is_safe(row):
    # Check if the row is already safe
    if is_increasing_or_decreasing(row) and has_valid_differences(row):
        return True


def calculate_safe_lists(list_of_lists) -> int:
    return sum(1 for row in list_of_lists if is_safe(row))


def is_safe_dampener(row):
    # Check if the row is already safe
    if is_increasing_or_decreasing(row) and has_valid_differences(row):
        return True
    # Check if removing one level makes it safe
    for i in range(len(row)):
        modified_row = row[:i] + row[i + 1:]  # Remove the i-th level
        if is_increasing_or_decreasing(modified_row) and has_valid_differences(
                modified_row):
            return True
    return False


def count_safe_reports(list_of_lists):
    return sum(1 for row in list_of_lists if is_safe(row))


def calculate_safe_lists_dampener(list_of_lists) -> int:
    return sum(1 for row in list_of_lists if is_safe_dampener(row))


def load_list_of_lists(filename):
    list_of_lists = []
    with open(filename, 'r') as file:
        for line in file:
            # Split by spaces and convert to integers
            row = line.strip().split()
            list_of_lists.append([int(num) for num in row])
    return list_of_lists


if __name__ == "__main__":
    file_path = 'input2.txt'
    list_of_lists = load_list_of_lists(file_path)
    print(f"Safe rows: {calculate_safe_lists(list_of_lists=list_of_lists)}")
    print(
        f"Safe dampener rows: {calculate_safe_lists_dampener(list_of_lists=list_of_lists)}"
    )


class TestCalculations(unittest.TestCase):

    def test_calculate_safe_lists(self):
        in_list = [[7, 6, 4, 2, 1], [1, 2, 7, 8, 9], [9, 7, 6, 2, 1],
                   [1, 3, 2, 4, 5], [8, 6, 4, 4, 1], [1, 3, 6, 7, 9]]
        self.assertEqual(calculate_safe_lists(in_list), 2)

    def test_safe_lists_dampener(self):
        in_list = [[7, 6, 4, 2, 1], [1, 2, 7, 8, 9], [9, 7, 6, 2, 1],
                   [1, 3, 2, 4, 5], [8, 6, 4, 4, 1], [1, 3, 6, 7, 9]]
        self.assertEqual(calculate_safe_lists_dampener(in_list), 4)


if __name__ == "__main__":
    unittest.main()
