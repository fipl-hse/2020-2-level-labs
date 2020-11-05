"""
Longest common subsequence implementation starter
"""
from main import tokenize_by_lines
from main import create_zero_matrix
from main import fill_lcs_matrix
from main import find_lcs_length
from main import find_lcs
from main import calculate_plagiarism_score
from main import calculate_text_plagiarism_score

if __name__ == '__main__':
    original_text = 'The cat appeared! The dog disappeared!'
    suspicious_text = 'The man arrived! The boy left...'
    print('Original text: {}\nSuspicious text: {}'.format(original_text, suspicious_text))

    original_text_tokens = tokenize_by_lines(original_text)
    suspicious_text_tokens = tokenize_by_lines(suspicious_text)
    print(original_text_tokens, suspicious_text_tokens)

    zero_matrix = create_zero_matrix(len(original_text), len(suspicious_text))
    print('Zero matrix: {}'.format(zero_matrix))

    lcs_matrix = fill_lcs_matrix(original_text_tokens[0], suspicious_text_tokens[0])
    print('LCS matrix: {}'.format(lcs_matrix))

    lcs_length = find_lcs_length(original_text_tokens[0], suspicious_text_tokens[0], plagiarism_threshold=0.3)
    print('LCS length: {}'.format(lcs_length))

    lcs = find_lcs(original_text_tokens[0], suspicious_text_tokens[0], lcs_matrix)
    print('LCS is {}'.format(lcs))

    plagiarism_score = calculate_plagiarism_score(lcs_length, suspicious_text_tokens[0])
    print('The score of plagiarism is {}'.format(plagiarism_score))

    text_plagiarism_score = calculate_text_plagiarism_score\
        (original_text_tokens, suspicious_text_tokens, plagiarism_threshold=0.3)
    print('The score is: {}% of plagiarism.'.format(round(text_plagiarism_score * 100, 2)))

    RESULT = text_plagiarism_score

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == 0.3333333333333333, 'Checking not working'