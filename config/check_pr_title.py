# pylint: skip-file
import argparse
import sys

TEMPLATE = ''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Checks that PR name is done using the template')
    parser.add_argument('--pr-name', type=str, help='Current PR name')
    args: argparse.Namespace = parser.parse_args()
    print(args.pr_name)
    sys.exit(0)
