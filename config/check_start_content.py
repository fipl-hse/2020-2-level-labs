"""
Some simple checks for start.py lab files
"""

import argparse
import sys
import os


def check_assert_line(content: str) -> bool:
    expected = 'assert RESULT'
    return expected in content


def parse_main_file_functions(text: str) -> list:
    functions = []
    for function in text.split('def'):
        title = ''
        for element in function:
            if element == '(':
                break
            title += element
        functions.append(title[1:])
    return functions[1:]


def check_start_file_called_functions(text: str, functions: list) -> bool:
    print(text)
    print(functions)
    for function in functions[:-1]:
        print(f'checking {function}')
        if function[:-8] not in text:
            return False
    return True


def get_target_functions(path: str) -> list:
    with open(path, 'r', encoding='utf-8') as functions:
        return functions.read().split('\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Checks start.py files and tests them')
    parser.add_argument('--start_py_content', type=str, help='Content of start.py for each lab')
    parser.add_argument('--functions', type=str, help='Functions called in start.py for each lab')
    parser.add_argument('--target', type=str, help='Functions for current mark')
    args: argparse.Namespace = parser.parse_args()

    if check_assert_line(args.start_py_content):
        print('Passed assert RESULT statement')
        # sys.exit(0)
    else:
        print('Make sure you made assert RESULT in start.py file')
        sys.exit(1)

    if check_start_file_called_functions(args.functions, get_target_functions(args.target)):
        print('Passed calling functions check')
        sys.exit(0)
    else:
        print('Make sure you called all implemented functions in start.py file')
        sys.exit(1)

# Test: a) assert concordance_realize is in file
# Test: b) call start.py, expect it does not throw Error
