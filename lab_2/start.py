"""
Longest common subsequence implementation starter
"""
import main

original_text = 'Her cats are big and nice.\nThey love eating Whiskas.'
suspicious_text = 'His dogs are big and cute.\nThey love eating Pegigri!'

orig_tokens = main.tokenize_by_lines(original_text)
susp_tokens = main.tokenize_by_lines(suspicious_text)

print(f"Original text tokens: {orig_tokens}\nSuspicious text tokens: {susp_tokens}\n")
print('=================================\n')

orig_sent_1 = orig_tokens[0]
susp_sent_1 = susp_tokens[0]

lcs_matrix = main.fill_lcs_matrix(orig_sent_1, susp_sent_1)
print(f"{orig_sent_1}\n{susp_sent_1}\nLCS matrix:")

for row in lcs_matrix:
    print(row)

print('=================================\n')

lcs_len = main.find_lcs_length(orig_sent_1, susp_sent_1, 0.3)
print(f"LCS len: {lcs_len}\n")
print('=================================\n')

lcs = main.find_lcs(orig_sent_1, susp_sent_1, lcs_matrix)
print(f"LCS for the first sentences: {lcs}\n")
print('=================================\n')

plagiarism_score = main.calculate_plagiarism_score(lcs_len, susp_sent_1)
print(f"The plagiarism score for the first sentence: {plagiarism_score}\n")
print('=================================\n')

plagiarism_text = main.calculate_text_plagiarism_score(orig_tokens, susp_tokens)
print(f"The plagiarism score for the text: {plagiarism_text}\n")
print('=================================\n')

diff_in_sentence = main.find_diff_in_sentence(orig_sent_1, susp_sent_1, lcs)
print(f"The difference in first sentences: {diff_in_sentence}\n")
print('=================================\n')

stats = main.accumulate_diff_stats(orig_tokens, susp_tokens)
print(f"Here are the statistics information:\n{stats}\n")
print('=================================\n')

report = main.create_diff_report(orig_tokens, susp_tokens, stats)
print(f"The report for two texts:\n{report}\n")
print('=================================')

RESULT = report
assert RESULT, 'Not working'
