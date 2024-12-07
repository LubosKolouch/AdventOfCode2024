import sys
import unittest
from itertools import product


def can_reach_target(target: int, numbers: list[int]) -> bool:
    """
    Part One functionality:
    Given a target integer and a list of integers, determine if by inserting
    '+' or '*' between them (in order), evaluated strictly left-to-right, we can produce the target.
    """
    if len(numbers) == 1:
        return numbers[0] == target

    # Each operator position can be '+' or '*'
    for ops_pattern in product(['+', '*'], repeat=len(numbers) - 1):
        current_value = numbers[0]
        for i, op in enumerate(ops_pattern, start=1):
            if op == '+':
                current_value = current_value + numbers[i]
            else:  # '*'
                current_value = current_value * numbers[i]
        if current_value == target:
            return True
    return False


def can_reach_target_with_all_ops(target: int, numbers: list[int]) -> bool:
    """
    Part Two functionality:
    Given a target integer and a list of integers, determine if by inserting
    '+', '*', or '||' (concatenate) between them (in order), evaluated strictly
    left-to-right, we can produce the target.
    """
    if len(numbers) == 1:
        return numbers[0] == target

    # Each operator position can be '+', '*', or '||'
    for ops_pattern in product(['+', '*', '||'], repeat=len(numbers) - 1):
        current_value = numbers[0]
        for i, op in enumerate(ops_pattern, start=1):
            if op == '+':
                current_value = current_value + numbers[i]
            elif op == '*':
                current_value = current_value * numbers[i]
            else:  # '||' concatenate
                current_value = int(str(current_value) + str(numbers[i]))
        if current_value == target:
            return True
    return False


def solve_equations(equations: list[str], part2: bool = False) -> int:
    """
    Solve equations for either part1 or part2.
    If part2 is False, only '+' and '*' are used.
    If part2 is True, '+', '*', and '||' are used.
    """
    total = 0
    for eq in equations:
        eq = eq.strip()
        if not eq:
            continue
        target_str, nums_str = eq.split(':')
        target = int(target_str.strip())
        numbers = list(map(int, nums_str.strip().split()))

        if part2:
            # Use all operators
            if can_reach_target_with_all_ops(target, numbers):
                total += target
        else:
            # Use only + and *
            if can_reach_target(target, numbers):
                total += target
    return total


class TestPart1(unittest.TestCase):

    def test_example(self):
        example_lines = [
            "190: 10 19", "3267: 81 40 27", "83: 17 5", "156: 15 6",
            "7290: 6 8 6 15", "161011: 16 10 13", "192: 17 8 14",
            "21037: 9 7 18 13", "292: 11 6 16 20"
        ]
        # Part One: only three are solvable: 190, 3267, 292 sum=3749
        self.assertEqual(solve_equations(example_lines, part2=False), 3749)

    def test_no_obstacles(self):
        # Simple test for part1
        lines = ["100: 100", "50: 100"]
        # Only 100:100 works directly
        self.assertEqual(solve_equations(lines, part2=False), 100)


class TestPart2(unittest.TestCase):

    def test_example(self):
        example_lines = [
            "190: 10 19", "3267: 81 40 27", "83: 17 5", "156: 15 6",
            "7290: 6 8 6 15", "161011: 16 10 13", "192: 17 8 14",
            "21037: 9 7 18 13", "292: 11 6 16 20"
        ]
        # Part Two: six equations are solvable (190,3267,292 plus 156,7290,192)
        # sum=11387
        self.assertEqual(solve_equations(example_lines, part2=True), 11387)

    def test_concatenation(self):
        lines = ["1234: 12 34", "999: 9 9 9"]
        # "1234: 12 34" = 12||34=1234
        # "999: 9 9 9" can do 9||9||9=999
        self.assertEqual(solve_equations(lines, part2=True), 1234 + 999)


def main_part1():
    # Reads from 'input7.txt' and solves part1
    with open('input7.txt') as f:
        equations = f.readlines()
    result = solve_equations(equations, part2=False)
    print(result)


def main_part2():
    # Reads from 'input7.txt' and solves part2
    with open('input7.txt') as f:
        equations = f.readlines()
    result = solve_equations(equations, part2=True)
    print(result)


if __name__ == '__main__':
    # Usage:
    # python script.py part1 -> run part1 with input7.txt
    # python script.py part2 -> run part2 with input7.txt
    # python script.py -> run tests
    if len(sys.argv) > 1 and sys.argv[1] == 'part1':
        main_part1()
    elif len(sys.argv) > 1 and sys.argv[1] == 'part2':
        main_part2()
    else:
        unittest.main()
