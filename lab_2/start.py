"""
Longest common subsequence implementation starter
"""

from main import tokenize_by_lines
from main import calculate_text_plagiarism_score

if __name__ == '__main__':
    original_text = '''I have a cat.
    It is Garfield.
    Garfield is fond of running and jumping.'''
    suspicious_text = '''I have a dog.
    It is Bim.
    Bim enjoys running.
    I love my pet so much!!!'''

    print('Original text is:\n', original_text)
    print()
    print('This text suspiciously looks like it.\n', suspicious_text)

    original_text_tokens = tokenize_by_lines(original_text)
    suspicious_text_tokens = tokenize_by_lines(suspicious_text)

    print('\n...Checking on plagiarism...\n')
    plagiarism_result = calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens,
                                                        plagiarism_threshold=0.3)
    print(plagiarism_result)
    print('The result is: {}% of plagiarism.'.format(round(plagiarism_result * 100, 2)))

    RESULT = plagiarism_result

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == 0.35416666666666663, 'Checking not working'
