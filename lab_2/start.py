"""
Longest common subsequence implementation starter
"""
from lab_2 import main
if __name__ == "__main__":
    original_text_tokens = (('the', 'frog', 'sleeping'),
                            ('the', 'kitten', 'running'))
    suspicious_text_tokens = (('the', 'girl', 'likes'),
                              ('the', 'woman', 'dislikes'))
    plagiarism_threshold = 0.3
    lcs_matrix = main.fill_lcs_matrix(original_text_tokens, suspicious_text_tokens)
    lcs_length = main.find_lcs_length(original_text_tokens, suspicious_text_tokens, plagiarism_threshold)
    lcs = main.find_lcs(original_text_tokens, suspicious_text_tokens, lcs_matrix)
    calculate_plagiarism_score = main.calculate_plagiarism_score(lcs_length, suspicious_text_tokens)
    text_plagiarism_score = main.calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens, plagiarism_threshold)
    expected = expected = (1 / 3 + 1 / 3) / 2
    actual = text_plagiarism_score

    RESULT = actual
    assert RESULT == expected, "Calculate plagiarism score not working"

