"""
Longest common subsequence implementation starter
"""
import main

ORIGINAL_TEXT = '''The dog is barking.
It has black nose and big teeth.'''
SUSPICIOUS_TEXT = '''The big dog is sleeping.
He has black nose and lovely paws.'''
orig_tokens = main.tokenize_by_lines(ORIGINAL_TEXT)
susp_tokens = main.tokenize_by_lines(SUSPICIOUS_TEXT)

print("Here is tokenized original text:", orig_tokens)
print("Here is tokenized suspicious text:", susp_tokens)

lcs_length = main.find_lcs_length(orig_tokens, susp_tokens, plagiarism_threshold=0.0)
print("Here is the length of the longest common subsequence:", lcs_length)

matrix = main.fill_lcs_matrix(orig_tokens, susp_tokens)

lcs = main.find_lcs(orig_tokens, susp_tokens, matrix)
print("Here is the longest common subsequence:", lcs)

plagiarism_score = main.calculate_plagiarism_score(lcs_length, susp_tokens)
print("The plagiarism score:", plagiarism_score)

text_plagiarism_score = main.calculate_text_plagiarism_score(orig_tokens, susp_tokens, plagiarism_score)
print("Text average percent of plagiarism:", text_plagiarism_score)

RESULT = text_plagiarism_score
assert RESULT, 'Not working'
