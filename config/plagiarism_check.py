"""
Module to check plagiarism rate compared to other files
"""
import ast
import os
import sys

import argparse
import pycode_similar


def get_cli_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--source-dir',
                        help='Check this directory for duplications' +
                        '\n For example, lab1_frequencies_counter',
                        type=str,
                        required=True)

    parser.add_argument('--others-dir',
                        help='PR data from others',
                        type=str,
                        required=True)
    return parser


def get_python_files_from(path):
    files_paths = []
    for root, _, files in os.walk(path):
        path = root.split(os.sep)
        for f_name in files:
            if f_name.endswith('.py') and f_name != '__init__.py' and '_test' not in f_name:
                print(f_name)
                files_paths.append(os.path.join(root, f_name))
    return files_paths


def compare_file_to_others(ref_file, candidate_files):
    files = [ref_file, ]
    files.extend(candidate_files)
    print(files)
    payload = []
    for name in files:
        try:
            content = read_file_content(name)
            _ = ast.parse(content)
            payload.append(content)
        except SyntaxError:
            pass

    res = pycode_similar.detect(payload, diff_method=pycode_similar.UnifiedDiff)
    per_function_reports = res[0][1]
    if not per_function_reports:
        return 0
    total = 0
    for i in per_function_reports:
        total += i.plagiarism_percent
    return total / len(per_function_reports)


def read_file_content(path):
    with open(path) as opened_file:
        return opened_file.read()


def main():
    argv = get_cli_parser().parse_args()

    source_files = get_python_files_from(argv.source_dir)
    other_files = get_python_files_from(argv.others_dir)

    avg = 0
    for source in source_files:
        avg += compare_file_to_others(source, other_files)
    avg /= len(source_files)

    print('Plagiarism ratio is: {}'.format(avg))
    if avg > 0.3:
        print('Too much. Write code yourself')
        return 1
    print('Well done!')
    return 0


if __name__ == '__main__':
    sys.exit(main())
