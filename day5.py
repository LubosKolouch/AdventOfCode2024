from typing import List, Dict, Set, Tuple
import unittest

def parse_input(input_str: str) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    """
    Parses the input string into ordering rules and updates.

    Args:
        input_str: The raw input string containing ordering rules and updates.

    Returns:
        A tuple containing a list of ordering rules and a list of updates.
    """
    lines = input_str.strip().split('\n')
    ordering_rules = []
    updates = []
    is_update_section = False

    for line in lines:
        line = line.strip()
        if not line:
            is_update_section = True
            continue
        if not is_update_section:
            x, y = map(int, line.split('|'))
            ordering_rules.append((x, y))
        else:
            update = list(map(int, line.split(',')))
            updates.append(update)

    return ordering_rules, updates

def is_update_correct(ordering_rules: List[Tuple[int, int]], update: List[int]) -> bool:
    """
    Checks if an update is correctly ordered according to the given ordering rules.

    Args:
        ordering_rules: A list of tuples representing the ordering rules.
        update: A list of page numbers representing the update.

    Returns:
        True if the update is correctly ordered, False otherwise.
    """
    page_indices = {page: idx for idx, page in enumerate(update)}
    for x, y in ordering_rules:
        if x in page_indices and y in page_indices:
            if page_indices[x] >= page_indices[y]:
                return False
    return True

def find_middle_page(update: List[int]) -> int:
    """
    Finds the middle page number of an update.

    Args:
        update: A list of page numbers representing the update.

    Returns:
        The middle page number.
    """
    middle_index = len(update) // 2
    return update[middle_index]

def sum_of_middle_pages(ordering_rules: List[Tuple[int, int]], updates: List[List[int]]) -> int:
    """
    Calculates the sum of middle page numbers of correctly ordered updates.

    Args:
        ordering_rules: A list of tuples representing the ordering rules.
        updates: A list of updates, each update is a list of page numbers.

    Returns:
        The sum of middle page numbers of correctly ordered updates.
    """
    total = 0
    for update in updates:
        if is_update_correct(ordering_rules, update):
            total += find_middle_page(update)
    return total

def correct_update_order(ordering_rules: List[Tuple[int, int]], update: List[int]) -> List[int]:
    """
    Corrects the order of an update according to the ordering rules.

    Args:
        ordering_rules: A list of tuples representing the ordering rules.
        update: A list of page numbers representing the update.

    Returns:
        A list of page numbers in the correct order.
    """
    # Build a graph of dependencies
    graph: Dict[int, Set[int]] = {page: set() for page in update}
    in_degree: Dict[int, int] = {page: 0 for page in update}

    # Only consider ordering rules that involve pages in the update
    for x, y in ordering_rules:
        if x in update and y in update:
            graph[x].add(y)
            in_degree[y] += 1

    # Kahn's algorithm for topological sorting
    from collections import deque

    queue = deque([page for page in update if in_degree[page] == 0])
    sorted_update = []

    while queue:
        page = queue.popleft()
        sorted_update.append(page)
        for neighbor in graph[page]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_update) != len(update):
        raise ValueError("Cycle detected in ordering rules.")

    return sorted_update

def sum_of_corrected_middle_pages(ordering_rules: List[Tuple[int, int]], updates: List[List[int]]) -> int:
    """
    Calculates the sum of middle page numbers after correcting the order of incorrectly ordered updates.

    Args:
        ordering_rules: A list of tuples representing the ordering rules.
        updates: A list of updates, each update is a list of page numbers.

    Returns:
        The sum of middle page numbers after correcting the order of incorrectly ordered updates.
    """
    total = 0
    for update in updates:
        if not is_update_correct(ordering_rules, update):
            corrected_update = correct_update_order(ordering_rules, update)
            total += find_middle_page(corrected_update)
    return total

class TestPrintQueue(unittest.TestCase):
    """Unit tests for the print queue problem."""

    def setUp(self):
        """Set up test variables."""
        self.sample_input = """
        47|53
        97|13
        97|61
        97|47
        75|29
        61|13
        75|53
        29|13
        97|29
        53|29
        61|53
        97|53
        61|29
        47|13
        75|47
        97|75
        47|61
        75|61
        47|29
        75|13
        53|13

        75,47,61,53,29
        97,61,53,29,13
        75,29,13
        75,97,47,61,53
        61,13,29
        97,13,75,29,47
        """
        self.ordering_rules, self.updates = parse_input(self.sample_input)

    def test_parse_input(self):
        """Test parsing of input."""
        expected_rules = [
            (47, 53), (97, 13), (97, 61), (97, 47), (75, 29), (61, 13),
            (75, 53), (29, 13), (97, 29), (53, 29), (61, 53), (97, 53),
            (61, 29), (47, 13), (75, 47), (97, 75), (47, 61), (75, 61),
            (47, 29), (75, 13), (53, 13)
        ]
        expected_updates = [
            [75, 47, 61, 53, 29],
            [97, 61, 53, 29, 13],
            [75, 29, 13],
            [75, 97, 47, 61, 53],
            [61, 13, 29],
            [97, 13, 75, 29, 47]
        ]
        self.assertEqual(self.ordering_rules, expected_rules)
        self.assertEqual(self.updates, expected_updates)

    def test_is_update_correct(self):
        """Test checking if updates are correctly ordered."""
        self.assertTrue(is_update_correct(self.ordering_rules, [75, 47, 61, 53, 29]))
        self.assertTrue(is_update_correct(self.ordering_rules, [97, 61, 53, 29, 13]))
        self.assertTrue(is_update_correct(self.ordering_rules, [75, 29, 13]))
        self.assertFalse(is_update_correct(self.ordering_rules, [75, 97, 47, 61, 53]))
        self.assertFalse(is_update_correct(self.ordering_rules, [61, 13, 29]))
        self.assertFalse(is_update_correct(self.ordering_rules, [97, 13, 75, 29, 47]))

    def test_find_middle_page(self):
        """Test finding the middle page of an update."""
        self.assertEqual(find_middle_page([75, 47, 61, 53, 29]), 61)
        self.assertEqual(find_middle_page([97, 61, 53, 29, 13]), 53)
        self.assertEqual(find_middle_page([75, 29, 13]), 29)
        self.assertEqual(find_middle_page([75, 97, 47, 61, 53]), 47)
        self.assertEqual(find_middle_page([61, 13, 29]), 13)
        self.assertEqual(find_middle_page([97, 13, 75, 29, 47]), 75)

    def test_sum_of_middle_pages(self):
        """Test calculating the sum of middle pages of correctly ordered updates."""
        total = sum_of_middle_pages(self.ordering_rules, self.updates)
        self.assertEqual(total, 143)

    def test_correct_update_order(self):
        """Test correcting the order of incorrectly ordered updates."""
        corrected_update1 = correct_update_order(self.ordering_rules, [75, 97, 47, 61, 53])
        self.assertEqual(corrected_update1, [97, 75, 47, 61, 53])

        corrected_update2 = correct_update_order(self.ordering_rules, [61, 13, 29])
        self.assertEqual(corrected_update2, [61, 29, 13])

        corrected_update3 = correct_update_order(self.ordering_rules, [97, 13, 75, 29, 47])
        self.assertEqual(corrected_update3, [97, 75, 47, 29, 13])

    def test_sum_of_corrected_middle_pages(self):
        """Test calculating the sum of middle pages after correcting updates."""
        total = sum_of_corrected_middle_pages(self.ordering_rules, self.updates)
        self.assertEqual(total, 123)

def main():
    """Main function to process the input file and calculate the result for both parts."""
    with open('input5.txt', 'r') as file:
        input_str = file.read()
    ordering_rules, updates = parse_input(input_str)

    # Part One
    total_correct = sum_of_middle_pages(ordering_rules, updates)
    print(f"Part One - Sum of middle page numbers: {total_correct}")

    # Part Two
    total_corrected = sum_of_corrected_middle_pages(ordering_rules, updates)
    print(f"Part Two - Sum of middle page numbers after correction: {total_corrected}")

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'run':
        main()
    else:
        unittest.main()
