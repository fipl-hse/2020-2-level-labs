# pylint: skip-file
import argparse
import re
import sys


def transform_score_into_lint(target_score: int) -> int:
    if target_score == 10 or target_score == 8:
        return 10
    elif target_score == 6:
        return 7
    elif target_score == 4:
        return 5
    else:
        return 0


def is_passed(lint_output: str, target_lint_level: int) -> int:
    lint_level = re.search(r'Your code has been rated at \d+\.\d+', lint_output).group(0)
    lint_score = int(re.search(r'\d+', lint_level).group(0))

    if lint_score < target_lint_level:
        print('\nLint check is not passed!')
        print('Fix the following issues and try again.\n')
        print(lint_output)
        return 1
    elif lint_score != 10:
        print('\nLint check passed but there are thing to improve:\n')
        print(lint_output)
        return 0
    else:
        print('\nLint check passed!\n')
        return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Processes lint output and determines whether lint level is passed')
    parser.add_argument('--lint-output', type=str, help='Output from pylint command')
    parser.add_argument('--target-score', type=int, help='Target score')
    args: argparse.Namespace = parser.parse_args()

    target_lint_level = transform_score_into_lint(args.target_score)
    if not target_lint_level:
        print('\nInvalid value for target score: accepted are 4, 6, 8, 10.\n')
        sys.exit(target_lint_level)

    sys.exit(is_passed(args.lint_output, target_lint_level))
