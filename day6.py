import sys
import unittest
from typing import List, Tuple

def find_guard_start_and_direction(grid: List[str]) -> Tuple[int, int, int]:
    direction_map = {'^': 0, '>': 1, 'v': 2, '<': 3}
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] in direction_map:
                return r, c, direction_map[grid[r][c]]
    return None, None, None

def simulate_guard_part1(grid: List[str]) -> int:
    """
    Part One simulation:
    Simulates the guard's movement and returns the number of unique positions visited.
    The guard moves until it steps off the map.
    
    Movement Rules:
    - If there's an obstacle '#' or going forward would leave the map, turn right (90 degrees).
    - Otherwise, step forward.
    """
    DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    start_r, start_c, dir_idx = find_guard_start_and_direction(grid)

    visited = set()
    visited.add((start_r, start_c))
    current_r, current_c = start_r, start_c

    while True:
        dr, dc = DIRECTIONS[dir_idx]
        front_r = current_r + dr
        front_c = current_c + dc

        # Check if next step goes off map
        if not (0 <= front_r < rows and 0 <= front_c < cols):
            # Guard leaves the map
            break

        # Check obstacle
        if grid[front_r][front_c] == '#':
            # Turn right
            dir_idx = (dir_idx + 1) % 4
            continue

        # Move forward
        current_r, current_c = front_r, front_c
        visited.add((current_r, current_c))

    return len(visited)

def simulate_with_loop_detection(grid: List[str]) -> Tuple[bool, int]:
    """
    Part Two simulation with loop detection:
    Simulates the guard's movement and detects if the guard gets stuck in a loop.
    Returns:
      (loop_detected, visited_count)
      
    loop_detected = True if the guard eventually revisits the same position and direction.
    visited_count = number of distinct cells visited.
    """
    DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    start_r, start_c, dir_idx = find_guard_start_and_direction(grid)
    visited_positions = set()
    visited_positions.add((start_r, start_c))
    current_r, current_c = start_r, start_c

    visited_states = set()  # (r, c, dir_idx)

    while True:
        state = (current_r, current_c, dir_idx)
        if state in visited_states:
            # Loop detected
            return True, len(visited_positions)
        visited_states.add(state)

        dr, dc = DIRECTIONS[dir_idx]
        front_r = current_r + dr
        front_c = current_c + dc

        # Check if stepping forward goes off the map
        if not (0 <= front_r < rows and 0 <= front_c < cols):
            # Guard leaves the map, no loop
            return False, len(visited_positions)

        # Check obstacle
        if grid[front_r][front_c] == '#':
            # Turn right
            dir_idx = (dir_idx + 1) % 4
            continue

        # Move forward
        current_r, current_c = front_r, front_c
        visited_positions.add((current_r, current_c))

def count_loop_positions(grid: List[str]) -> int:
    """
    For Part Two:
    Counts how many '.' positions (excluding guard's start) can be changed to '#'
    to cause the guard to loop instead of leaving the map.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    grid_list = [list(row) for row in grid]
    start_r, start_c, _ = find_guard_start_and_direction(grid)

    loop_count = 0
    for r in range(rows):
        for c in range(cols):
            # Cannot place obstruction at guard's start
            if (r == start_r and c == start_c):
                continue
            if grid_list[r][c] == '.':
                original = grid_list[r][c]
                grid_list[r][c] = '#'
                modified_grid = ["".join(row) for row in grid_list]
                loop_detected, _ = simulate_with_loop_detection(modified_grid)
                if loop_detected:
                    loop_count += 1
                # Restore
                grid_list[r][c] = original

    return loop_count

class TestPart1(unittest.TestCase):
    def test_example_given(self):
        # Example from the puzzle description for part one
        example_map = [
            "....#.....",
            ".........#",
            "..........",
            "..#.......",
            ".......#..",
            "..........",
            ".#..^.....",
            "........#.",
            "#.........",
            "......#..."
        ]
        # According to the example, the guard visits 41 distinct positions
        self.assertEqual(simulate_guard_part1(example_map), 41)

    def test_no_obstacles(self):
        # Simple map with no obstacles; guard faces up and will leave immediately
        grid = [
            "..^..",
            ".....",
            "....."
        ]
        # Guard starts at (0,2), facing up.
        # Next move is off the map.
        # Only the start position is visited.
        self.assertEqual(simulate_guard_part1(grid), 1)

    def test_immediate_obstacle(self):
        # Guard starts facing a wall directly
        grid = [
            "#^#",
            "###",
            "###"
        ]
        # Guard at (0,1) facing up. Above is off map, so guard stops immediately.
        # Only start visited.
        self.assertEqual(simulate_guard_part1(grid), 1)

class TestPart2(unittest.TestCase):
    def test_part2_small_scenario(self):
        # A small scenario for part two
        grid = [
            "^..."
        ]
        # Guard tries to move up and leaves immediately.
        # No loops possible no matter where we place an obstacle (except start).
        self.assertEqual(count_loop_positions(grid), 0)

def main_part1():
    # Reads from 'input6.txt' and prints part1 result (number of distinct visited positions)
    with open('input6.txt', 'r') as f:
        grid = [line.rstrip('\n') for line in f]
    result = simulate_guard_part1(grid)
    print(result)

def main_part2():
    # Reads from 'input6.txt' and prints part2 result (number of positions causing loops)
    with open('input6.txt', 'r') as f:
        grid = [line.rstrip('\n') for line in f]
    result = count_loop_positions(grid)
    print(result)

if __name__ == '__main__':
    # Usage:
    # python solution.py             -> runs tests
    # python solution.py part1 run   -> runs part1 with input6.txt
    # python solution.py part2 run   -> runs part2 with input6.txt
    if len(sys.argv) > 2 and sys.argv[1] == 'part1' and sys.argv[2] == 'run':
        main_part1()
    elif len(sys.argv) > 2 and sys.argv[1] == 'part2' and sys.argv[2] == 'run':
        main_part2()
    else:
        unittest.main()
