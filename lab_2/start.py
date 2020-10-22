"""
Longest common subsequence implementation starter
"""
from main import *


if __name__ == '__main__':
    original = 'I have a nice dog.'
    suspicious = 'I have a cute cat.'

    tokenized_original = tokenize_by_lines(original)
    tokenized_suspicious = tokenize_by_lines(suspicious)
    print(f"Original text tokens: {tokenized_original}\nSuspicious text tokens: {tokenized_suspicious}\n")

    zero_matrix_first = create_zero_matrix(len(tokenized_original), len(tokenized_suspicious))
    lcs_matrix = fill_lcs_matrix(tokenized_original, tokenized_suspicious)
    print(f"lcs matrix {lcs_matrix}\n")

    lcs_length = find_lcs_length(tokenized_original, tokenized_suspicious, 0.3)
    print(f"lcs length {lcs_length}\n")

    lcs = find_lcs(tokenized_original, tokenized_suspicious, lcs_matrix)
    print(f"lcs {lcs}\n")

    plagiarism_score = calculate_plagiarism_score(lcs_length, tokenized_suspicious)
    print(f"plagiarism score {plagiarism_score}\n")

    plagiarism_text = calculate_text_plagiarism_score(tokenized_original, tokenized_suspicious)
    print(f"plagiarism score for the text{plagiarism_text}\n")

    differences = find_diff_in_sentence(tokenized_original, tokenized_suspicious, lcs)
    print(f"differences {differences}\n")

    info = accumulate_diff_stats(tokenized_original, tokenized_suspicious)
    print(f"info about sentences in text\n{info}\n")

    report = create_diff_report(tokenized_original, tokenized_suspicious, info)
    print(f"The report for two texts:\n{report}")

    RESULT = tokenized_original

    assert RESULT == (('i', 'have', 'a', 'nice', 'dog'),)