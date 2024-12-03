import re
import unittest


def extract_and_compute(expression):
    # Regular expression to match valid mul instructions of the form mul(a,b)
    pattern = r"mul\((\d+),(\d+)\)"
    matches = re.findall(pattern, expression)
    
    # Perform multiplication for each pair and sum the results
    result = sum(int(a) * int(b) for a, b in matches)
    return result


def compute_with_do_and_dont(memory):
    # Regular expressions to match valid instructions
    mul_pattern = r"mul\((\d+),(\d+)\)"
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"
    
    # Parse the memory string
    matches = re.finditer(rf"{mul_pattern}|{do_pattern}|{dont_pattern}", memory)
    
    # Initial state
    mul_enabled = True
    total_sum = 0
    
    # Process each instruction
    for match in matches:
        instruction = match.group(0)
        if instruction == "do()":
            mul_enabled = True
        elif instruction == "don't()":
            mul_enabled = False
        elif mul_enabled:
            # Check for mul(x, y)
            mul_match = re.match(mul_pattern, instruction)
            if mul_match:
                x, y = map(int, mul_match.groups())
                total_sum += x * y
    
    return total_sum


class TestCalculations(unittest.TestCase):

    def test_part1(self):
        content = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
        self.assertEqual(extract_and_compute(content), 161)

    def test_part2(self):
        content = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
        self.assertEqual(compute_with_do_and_dont(content), 48)


if __name__ == "__main__":
    file_path = 'input3.txt'

    with open('./input3.txt', 'r') as file:
        content = file.read()
        print(extract_and_compute(content))
        print(compute_with_do_and_dont(content))
