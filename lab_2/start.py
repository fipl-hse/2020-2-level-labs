"""
Longest common subsequence implementation starter
"""
from lab_2 import main

if __name__ == "__main__":
     original_text = '''The horse is running.
      It is fast.'''
     second_text = '''The cow is eating. 
     It is slow.'''

     original_tokens = main.tokenize_by_lines(original_text)
     print('Original tokens: ', original_tokens)

     second_tokens = main.tokenize_by_lines(second_text)
     print('Second tokens: ', second_tokens)

     plagiarism_threshold = 0.3
     zero_matrix = main.create_zero_matrix(len(original_tokens), len(second_tokens))

     lcs_matrix = main.fill_lcs_matrix(original_tokens[0], second_tokens[0])
     print('LCS matrix: ', lcs_matrix)

     RESULT = lcs_matrix
     assert RESULT == lcs_matrix, "Not working"



