"""
Longest common subsequence implementation starter
"""
import main
if __name__ == "__main__":
     original_text = '''I have a nice dog. His name is Bard'''
     suspicious_text = '''I have a really cute cat. Her name is Chika'''

     original_tokens = main.tokenize_by_lines(original_text)
     print('Original tokens: ', original_tokens)

     suspicious_tokens = main.tokenize_by_lines(suspicious_text)
     print('Suspicious tokens: ', suspicious_tokens)

     plagiarism_threshold = 0.3
     zero_matrix = main.create_zero_matrix(len(original_tokens), len(suspicious_tokens))

     lcs_matrix = main.fill_lcs_matrix(original_tokens[0], suspicious_tokens[0])
     print('LCS matrix: ', lcs_matrix)

     lcs_length = main.find_lcs_length(original_tokens[0], suspicious_tokens[0], plagiarism_threshold)
     print('LCS is', lcs_length)

     lcs = main.find_lcs(original_tokens[0], suspicious_tokens[0], lcs_matrix)
     print('LCS for the the first sentence: ', lcs)

     calculate_plagiarism_score = main.calculate_plagiarism_score(lcs_length, suspicious_tokens[0])
     print('Plagiarism score is', calculate_plagiarism_score)

     text_plagiarism_score = main.calculate_text_plagiarism_score(original_tokens[0], suspicious_tokens[0])
     print('Plagiarism score for the text is', text_plagiarism_score)

     RESULT = text_plagiarism_score
     assert RESULT == text_plagiarism_score, "Not working"

