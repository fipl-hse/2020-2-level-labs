"""
Longest common subsequence implementation starter
"""
import main

if __name__ == '__main__':
    original_text_tokens = ('the', 'white', 'mouse', 'is', 'sleeping')
    suspicious_text_tokens = ('the', 'white', 'cat', 'is', 'eating')

    plagiarism_threshold = 0.3
    lcs_matrix = main.fill_lcs_matrix(original_text_tokens, suspicious_text_tokens)
    lcs_length = main.find_lcs_length(original_text_tokens, suspicious_text_tokens,plagiarism_threshold)
    lcs = main.find_lcs(original_text_tokens, suspicious_text_tokens, lcs_matrix)
    plagiarism_score = main.calculate_plagiarism_score(lcs_length, suspicious_text_tokens)
    text_plagiarism_score = main.calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens, plagiarism_threshold)
    diff_in_sentence = main.find_diff_in_sentence(original_sentence_tokens, suspicious_sentence_tokens, lcs)
    diff_stats = main.accumulate_diff_stats(original_text_tokens, suspicious_text_tokens, plagiarism_threshold)
    diff_report = main.create_diff_report(original_text_tokens, suspicious_text_tokens, accumulated_diff_stats)


    RESULT = diff_report

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Checking not working'