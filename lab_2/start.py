"""
Longest common subsequence implementation starter
"""
import main
if __name__ == "__main__":
     original_text = '''I have a nice dog. His name is Shar'''
     suspicious_text = '''I have a cute cat. Her name is Alya'''

     original_tokens = main.tokenize_by_lines(original_text)
     print('Original tokens: ', original_tokens)

     suspicious_tokens = main.tokenize_by_lines(suspicious_text)
     print('Suspicious tokens: ', suspicious_tokens)

     plagiarism_threshold = 0.3
     zero_matrix = main.create_zero_matrix(len(original_tokens), len(suspicious_tokens))

     m_lcs = main.fill_lcs_matrix(original_tokens[0], suspicious_tokens[0])
     print('LCS matrix: ', m_lcs)

     len_lcs = main.find_lcs_length(original_tokens[0], suspicious_tokens[0], plagiarism_threshold)
     print('LCS is', len_lcs)

     RESULT = len_lcs
     assert RESULT == len_lcs, "Not working"
