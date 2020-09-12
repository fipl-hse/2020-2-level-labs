# pylint: skip-file
import argparse
import re
import sys


def is_passed(lint_output: str, minimum_lint_level: int):
    lint_level = re.search(r'Your code has been rated at \d+\.\d+', lint_output).group(0)
    lint_score = int(re.search(r'\d+', lint_level).group(0))

    if lint_score < minimum_lint_level:
        print('Link ')
        return 1
    elif lint_score != 10:
        print('Lint check passed but there are thing to improve:\n')
        print(lint_output)
        return 0
    else:
        print('Lint check passed!')
        return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Processes lint output and determines whether lint level is passed')
    parser.add_argument('--lint-output', type=str, help='Output from pylint command')
    parser.add_argument('--lint-level', type=int, help='Minimum lint score')
    args: argparse.Namespace = parser.parse_args()

    sys.exit(is_passed(args.lint_output, args.lint_level))
