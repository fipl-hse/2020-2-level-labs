"""
Longest common subsequence implementation starter
"""
from main import tokenize_by_lines
from main import calculate_text_plagiarism_score

if __name__ == '__main__':
    original_text = 'the dog is running'
    suspicious_text = 'the black cat is sleeping'


    print("Original text is: ", original_text)
    print("Suspicious text is: ", suspicious_text)

    original_text_tokens = tokenize_by_lines(original_text)
    suspicious_text_tokens = tokenize_by_lines(suspicious_text)

    lcs_length = find_lcs_length(original_text_tokens, suspicious_text_tokens, plagiarism_threshold=0.3)
    print("Length of the longest common subsequence:", lcs_length)

    matrix = fill_lcs_matrix(original_text_tokens, suspicious_text_tokens)

    lcs = find_lcs(original_text_tokens, suspicious_text_tokens, matrix)
    print("The longest common subsequence:", lcs)

    plagiarism_score = calculate_plagiarism_score(lcs_length, suspicious_text_tokens)
    print("The plagiarism score:", plagiarism_score)

    text_plagiarism_score = calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens, plagiarism_score)
    print("Text plagiarism score:", text_plagiarism_score)

    RESULT = text_plagiarism_score

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Not working'

