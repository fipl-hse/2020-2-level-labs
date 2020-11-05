"""
Longest common subsequence implementation starter
"""

import main


if __name__ == '__main__':
    with open('lab_2/diff_report_example.txt', 'r', encoding='utf-8') as file:
        report_example = file.read()
    original_text = 'I have a cat. \nIts body is covered with bushy white fur.'
    suspicious_text = 'I have a cat. \nIts body is covered with shiny black fur.'
    print('\tOriginal text:\n' + original_text)
    print('\n\tSuspicious text:\n' + suspicious_text)
    print('\n\t...tokenizing original text...')
    original_text_tokens = main.tokenize_by_lines(original_text)
    print('\t...tokenizing suspicious text...')
    suspicious_text_tokens = main.tokenize_by_lines(suspicious_text)
    print('\t...creating a line-by-line diff report...\n\n')
    report = (main.create_diff_report(original_text_tokens, suspicious_text_tokens,
                                      main.accumulate_diff_stats(original_text_tokens, suspicious_text_tokens)))
    print(report)

    RESULT = report
    assert RESULT == report_example, 'LCS implementation not working'
