"""
Some simple checks for start.py lab files
"""

import argparse
import sys


def check_assert_is_in_file(content: str):
    expected = 'assert RESULT'
    if expected in content:
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Checks start.py files and tests them')
    parser.add_argument('--start_py_content', type=str, help='Content of start.py for each lab')
    args: argparse.Namespace = parser.parse_args()

    if check_assert_is_in_file(args.start_py_content):
        print('Passed')
        sys.exit(0)
    print('Make sure you made assert RESULT in start.py file')
    sys.exit(1)


# Test: a) assert concordance_realize is in file
# Test: b) call start.py, expect it does not throw Error
