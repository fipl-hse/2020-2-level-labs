"""
Longest common subsequence implementation starter
"""
from main import find_lcs_length

sentence_first = ('the', 'dog', 'is', 'running', 'inside', 'the', 'house')
sentence_second = ('the', 'cat', 'is', 'sleeping', 'inside', 'the', 'house')

RESULT = find_lcs_length(sentence_first, sentence_second, 0.3)

assert RESULT, 'LCS_length not working'
