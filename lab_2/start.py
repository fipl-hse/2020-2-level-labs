"""
Longest common subsequence implementation starter
"""
import main

original_text_tokens = "I have a cat.\nIt's body is covered with bushy white fur."
suspicious_text_tokens = "I have a cat.\nIt's body is covered with shiny black fur."

first_sentence_tokens = main.tokenize_by_lines(original_text_tokens)
second_sentence_tokens = main.tokenize_by_lines(suspicious_text_tokens)
print(f'tokens:{first_sentence_tokens}, {second_sentence_tokens}')

matrix = main.create_zero_matrix(len(first_sentence_tokens[1]),len(second_sentence_tokens[1]))
lcs_matrix = main.fill_lcs_matrix(first_sentence_tokens[1], second_sentence_tokens[1])
print(f'matrix: {lcs_matrix}')

lcs_length = main.find_lcs_length(first_sentence_tokens[1], second_sentence_tokens[1], plagiarism_threshold = 0.3)
print(f'lcs_length: {lcs_length}')

lcs = main.find_lcs(first_sentence_tokens[1], second_sentence_tokens[1], lcs_matrix)
print(f'lcs: {lcs}')

plagiarism = main.calculate_plagiarism_score(lcs_length, second_sentence_tokens[1])
print(f'plagiarism: {plagiarism}')

text_plagiarism = main.calculate_text_plagiarism_score(first_sentence_tokens, second_sentence_tokens)
print(f'text plagiarism: {text_plagiarism}')

diff_in_sentence = main.find_diff_in_sentence(first_sentence_tokens[1], second_sentence_tokens[1], lcs)
print(f'diff_in_sentence: {diff_in_sentence}')

diff_stats = main.accumulate_diff_stats(first_sentence_tokens, second_sentence_tokens)
print(f'diff_stats: {diff_stats}')

report = main.create_diff_report(first_sentence_tokens, second_sentence_tokens, diff_stats)

RESULT = report.split()

assert RESULT == '''- i have a cat
+ i have a cat

lcs = 4, plagiarism = 100.0%

- its body is covered with | bushy white | fur
+ its body is covered with | shiny black | fur

lcs = 6, plagiarism = 75.0%

Text average plagiarism (words): 87.5%'''.split(), 'Lcs not working'


