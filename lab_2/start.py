"""
Longest common subsequence implementation starter
"""
from lab_2 import main

if __name__ == '__main__':
    original_text_tokens = ('the', 'black', 'dog', 'is', 'running')
    suspicious_text_tokens = ('the', 'black', 'cat', 'is', 'sleeping')

    plagiarism_threshold = 0.2
    lcs_matrix = main.fill_lcs_matrix(original_text_tokens, suspicious_text_tokens)
    lcs_length = main.find_lcs_length(original_text_tokens, suspicious_text_tokens,plagiarism_threshold)
    lcs = main.find_lcs(original_text_tokens, suspicious_text_tokens, lcs_matrix)

    RESULT = lcs_length

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Checking not working'

