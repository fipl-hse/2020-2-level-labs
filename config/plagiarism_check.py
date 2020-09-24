# pylint: skip-file
"""
Module to check plagiarism rate compared to other files
"""
import os
import sys
import ast
import argparse
import pycode_similar

from typing import List, Union


def get_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument('--source-file',
                        help='File to run plagiarism against',
                        type=str,
                        required=True)

    parser.add_argument('--others-dir',
                        help='Directory with files from other PRs',
                        type=str,
                        required=True)
    return parser


def get_python_files_from(path: str) -> list:
    files_paths = []
    for root, _, files in os.walk(path):
        for f_name in files:
            if f_name.endswith('.py') and f_name != '__init__.py' and '_test' not in f_name:
                print(f_name)
                files_paths.append(os.path.join(root, f_name))
    return files_paths


def compare_file_to_others(ref_file: str, candidate_files: List[str]) -> Union[int, float]:
    files = [ref_file, ]
    files.extend(candidate_files)
    file_contents = []
    for name in files:
        try:
            content = read_file_content(name)
            _ = ast.parse(content)
            file_contents.append(content)
        except SyntaxError:
            pass

    res = pycode_similar.detect(file_contents, diff_method=pycode_similar.UnifiedDiff)
    per_function_reports = res[0][1]
    if not per_function_reports:
        return 0
    total = 0
    for report in per_function_reports:
        total += report.plagiarism_percent
    return total / len(per_function_reports)


def read_file_content(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as opened_file:
        return opened_file.read()


def main() -> bool:
    argv = get_cli_parser().parse_args()

    source_file = argv.source_file
    other_files = get_python_files_from(argv.others_dir)

    avg = compare_file_to_others(source_file, other_files)

    print('Plagiarism ratio is: {}'.format(avg))
    if avg > 0.3:
        print('Too much. Write code yourself')
        return True
    print('Well done!')
    return False


if __name__ == '__main__':
    sys.exit(main())
