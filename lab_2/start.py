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

print(f"Here are original text tokens: {orig_tokens}\n Here are suspicious text tokens: {susp_tokens}\n")

orig_first_sent = orig_tokens[1]
susp_first_sent = susp_tokens[1]

zero_matrix_first = main.create_zero_matrix(len(orig_first_sent), len(susp_first_sent))
lcs_matrix = main.fill_lcs_matrix(orig_first_sent, susp_first_sent)
print(f" Here is LCS matrix: {lcs_matrix}\n")

lcs_len = main.find_lcs_length(orig_first_sent, susp_first_sent, 0.3)
print(f" Here is LCS  {lcs_len}\n")

lcs = main.find_lcs(orig_first_sent, susp_first_sent, lcs_matrix)
print(f"LCS for first sentences: {lcs}\n")

plagiarism_score = main.calculate_plagiarism_score(lcs_len, susp_first_sent)
print(f"THere is the plagiarism score: {plagiarism_score}\n")

plagiarism_text = main.calculate_text_plagiarism_score(orig_tokens, susp_tokens)
print(f"The plagiarism score for the text: {plagiarism_text}\n")

diff_in_sent = main.find_diff_in_sentence(orig_first_sent, susp_first_sent, lcs)
print(f" Here is the difference in sentences: {diff_in_sent}\n")

stats = main.accumulate_diff_stats(orig_tokens, susp_tokens)
print(f"Here are some statistics:\n{stats}\n")

report = main.create_diff_report(orig_tokens, susp_tokens, stats)
print(f"The report for two texts:\n{report}")

RESULT = report
assert RESULT, 'Not working'
