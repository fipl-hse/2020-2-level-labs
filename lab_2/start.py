"""
Longest common subsequence implementation starter
"""
from lab_2 import main
if __name__ == "__main__":
    origignal_text = "The cat is sleeping. So do Sam"
    suspicious_text = "The dog is eating. So do I"

    first_sentence_tokens = main.tokenize_by_lines(original_text)

    second_sentence_tokens = main.tokenize_by_lines(suspicious_text)

    plagiarism_threshold = 0.3
    zero_matrix = main.create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))

    plagiarism_threshold = 0.3
    zero_matrix = main.create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))

    lcs_matrix = main.fill_lcs_matrix(first_sentence_tokens[0], second_sentence_tokens[0])
    print('LCS matrix: ', lcs_matrix)

    lcs_length = main.find_lcs_length(first_sentence_tokens[0], second_sentence_tokens[0], plagiarism_threshold)
    print('LCS -', lcs_length)

    lcs = main.find_lcs(first_sentence_tokens[0], second_sentence_tokens[0], lcs_matrix)
    print('LCS for the the first sentence: ', lcs)

    calculate_plagiarism_score = main.calculate_plagiarism_score(lcs_length, second_sentence_tokens[0])
    print('Plagiarism score -', calculate_plagiarism_score)

    text_plagiarism_score = main.calculate_text_plagiarism_score(first_sentence_tokens[0], second_sentence_tokens[0])
    print('Plagiarism score for the text -', text_plagiarism_score)

    RESULT = text_plagiarism_score
    assert RESULT == text_plagiarism_score, "Sorry, currently not working"




