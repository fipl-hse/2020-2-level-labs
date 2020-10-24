"""
Longest common subsequence implementation starter
"""
from lab_2.main import tokenize_by_lines,create_zero_matrix, fill_lcs_matrix, \
    find_lcs_length, find_lcs, calculate_plagiarism_score, calculate_text_plagiarism_score

original_text = '''
Once upon a time a little cat Meow walked down the street.
She met her friend, a giant dog Bow.
And they continued their walk together.
'''
suspicious_text = '''
Once upon a time a giant dog Bow walked down the street.
He met his friend, a little cat Meow.
And they went to the theatre.
'''
plagiarism_threshold = 0.3
tuple_original = tokenize_by_lines(original_text)
tuple_suspicious = tokenize_by_lines(suspicious_text)
lcs_matrix = fill_lcs_matrix(tuple_original, tuple_suspicious)
lcs_length = find_lcs_length(tuple_original,tuple_suspicious,plagiarism_threshold)
max_subsequence = find_lcs(tuple_original, tuple_suspicious, lcs_matrix)
plagiarism = calculate_plagiarism_score(lcs_length, tuple_suspicious)
texts_plagiarism = calculate_text_plagiarism_score(tuple_original, tuple_suspicious, plagiarism_threshold)

RESULT = plagiarism
assert RESULT, 'Calculate plagiarism score not working'
