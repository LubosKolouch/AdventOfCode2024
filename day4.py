from typing import List, Tuple
import unittest

def count_word_occurrences(grid: List[List[str]], word: str) -> int:
    """
    Counts the number of occurrences of a word in a grid, considering all 8 possible directions.

    Args:
        grid: A 2D list of single-character strings representing the grid.
        word: The word to search for.

    Returns:
        The number of times the word occurs in the grid.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    if not word:
        return 0

    directions: List[Tuple[int, int]] = [
        (-1, -1),  # up-left
        (-1, 0),   # up
        (-1, 1),   # up-right
        (0, -1),   # left
        (0, 1),    # right
        (1, -1),   # down-left
        (1, 0),    # down
        (1, 1)     # down-right
    ]

    def is_valid_position(x: int, y: int) -> bool:
        return 0 <= x < rows and 0 <= y < cols

    def check_direction(x: int, y: int, dx: int, dy: int) -> bool:
        for k in range(len(word)):
            nx = x + dx * k
            ny = y + dy * k
            if not is_valid_position(nx, ny):
                return False
            if grid[nx][ny] != word[k]:
                return False
        return True

    count = 0
    for i in range(rows):
        for j in range(cols):
            for dx, dy in directions:
                if check_direction(i, j, dx, dy):
                    count += 1

    return count

def count_xmas_shapes(grid: List[List[str]]) -> int:
    """
    Counts the number of 'X-MAS' shapes in the grid. An 'X-MAS' shape consists of two overlapping
    'MAS' sequences forming an 'X', where each 'MAS' can be forwards or backwards.

    Args:
        grid: A 2D list of single-character strings representing the grid.

    Returns:
        The number of 'X-MAS' shapes found in the grid.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    def is_valid_position(x: int, y: int) -> bool:
        return 0 <= x < rows and 0 <= y < cols

    def check_diagonal(seq: List[str]) -> bool:
        return seq == ['M', 'A', 'S'] or seq == ['S', 'A', 'M']

    count = 0
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            center = grid[i][j]
            if center != 'A':
                continue

            # Check down-right diagonal
            dr_seq = []
            for k in range(-1, 2):
                x, y = i + k, j + k
                if not is_valid_position(x, y):
                    break
                dr_seq.append(grid[x][y])
            else:
                if not check_diagonal(dr_seq):
                    continue
            # Check down-left diagonal
            dl_seq = []
            for k in range(-1, 2):
                x, y = i + k, j - k
                if not is_valid_position(x, y):
                    break
                dl_seq.append(grid[x][y])
            else:
                if not check_diagonal(dl_seq):
                    continue
            # Both diagonals form 'MAS' or 'SAM'
            count += 1
    return count

class TestCountWordOccurrences(unittest.TestCase):
    """Unit tests for count_word_occurrences function."""

    def test_empty_grid(self):
        """Test with an empty grid."""
        grid = []
        word = "XMAS"
        self.assertEqual(count_word_occurrences(grid, word), 0)

    def test_single_letter_grid(self):
        """Test with a grid containing a single letter."""
        grid = [['X']]
        word = "X"
        self.assertEqual(count_word_occurrences(grid, word), 1)

    def test_no_occurrences(self):
        """Test when the word does not occur in the grid."""
        grid = [['A', 'B'], ['C', 'D']]
        word = "XMAS"
        self.assertEqual(count_word_occurrences(grid, word), 0)

    def test_single_occurrence(self):
        """Test when the word occurs once in the grid."""
        grid = [['X', 'M', 'A', 'S']]
        word = "XMAS"
        self.assertEqual(count_word_occurrences(grid, word), 1)

    def test_multiple_occurrences(self):
        """Test when the word occurs multiple times in the grid."""
        grid_str = """
        X M A S
        M X A S
        X M A X
        M A S X
        """
        grid = [line.strip().split() for line in grid_str.strip().split('\n')]
        word = "XMAS"
        result = count_word_occurrences(grid, word)
        self.assertEqual(result, 2)

    def test_puzzle_input(self):
        """Test with the provided puzzle input."""
        grid_str = """
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
        """
        grid = [list(line.strip()) for line in grid_str.strip().split('\n')]
        word = "XMAS"
        result = count_word_occurrences(grid, word)
        expected_count = 11
        self.assertEqual(result, expected_count)

class TestCountXmasShapes(unittest.TestCase):
    """Unit tests for count_xmas_shapes function."""

    def test_empty_grid(self):
        """Test with an empty grid."""
        grid = []
        self.assertEqual(count_xmas_shapes(grid), 0)

    def test_no_occurrences(self):
        """Test when there are no X-MAS shapes in the grid."""
        grid = [['A', 'B'], ['C', 'D']]
        self.assertEqual(count_xmas_shapes(grid), 0)

    def test_single_occurrence(self):
        """Test when there is one X-MAS shape in the grid."""
        grid = [
            ['M', 'X', 'S'],
            ['X', 'A', 'X'],
            ['S', 'X', 'M']
        ]
        self.assertEqual(count_xmas_shapes(grid), 1)

    def test_multiple_occurrences(self):
        """Test when there are multiple X-MAS shapes in the grid."""
        grid_str = """
        M S M S
        S A S A
        M S M S
        S A S A
        """
        grid = [line.strip().split() for line in grid_str.strip().split('\n')]
        result = count_xmas_shapes(grid)
        self.assertEqual(result, 4)

    def test_example_input(self):
        """Test with the example provided in the puzzle."""
        grid_str = """
        .M.S......
        ..A..MSMS.
        .M.S.MAA..
        ..A.ASMSM.
        .M.S.M....
        ..........
        S.S.S.S.S.
        .A.A.A.A..
        M.M.M.M.M.
        ..........
        """
        # Remove dots and replace with actual letters or skip
        grid = []
        for line in grid_str.strip().split('\n'):
            row = []
            for ch in line.strip():
                if ch != '.':
                    row.append(ch)
            grid.append(row)
        result = count_xmas_shapes(grid)
        self.assertEqual(result, 9)

    def test_puzzle_input(self):
        """Test with the puzzle input for Part Two."""
        with open('input4.txt', 'r') as file:
            grid = [list(line.strip()) for line in file if line.strip()]
        result = count_xmas_shapes(grid)
        expected_count = 28  # Replace with the correct count after calculation
        self.assertEqual(result, expected_count)

if __name__ == '__main__':
    import sys

    # Load input from 'input4.txt' if running as main
    if len(sys.argv) > 1 and sys.argv[1] == 'run':
        with open('input4.txt', 'r') as file:
            grid = [list(line.strip()) for line in file if line.strip()]
        word = "XMAS"
        part = sys.argv[2] if len(sys.argv) > 2 else 'part1'
        if part == 'part1':
            result = count_word_occurrences(grid, word)
            print(f"Part One - Number of occurrences of '{word}': {result}")
        elif part == 'part2':
            result = count_xmas_shapes(grid)
            print(f"Part Two - Number of 'X-MAS' shapes: {result}")
        else:
            print("Invalid part specified. Use 'part1' or 'part2'.")
    else:
        unittest.main()
