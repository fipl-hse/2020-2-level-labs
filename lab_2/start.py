"""
Longest common subsequence implementation starter
"""

import main
import copy

first_text = '''I have a cat.
It has eight limbs.
Its name is Octocat.'''

second_text = '''I have a lizard.
He has a long tail.
His name is Mister Lizard.'''

first_text = main.tokenize_by_lines(first_text)
second_text = main.tokenize_by_lines(second_text)
print(f'Here are the tokens for each text:\n{first_text}\n{second_text}')

lcs_matrix = main.fill_lcs_matrix(first_text[0], second_text[0])
lcs_matrix_with_tokens = copy.deepcopy(lcs_matrix)
lcs_matrix_with_tokens.insert(0, list(second_text[0]))
lcs_matrix_with_tokens[0].insert(0, 0)
for i in range(1, len(lcs_matrix_with_tokens)):
    lcs_matrix_with_tokens[i].insert(0, first_text[0][i-1])
format_row = '{:<5}' * len(lcs_matrix_with_tokens[0])
print('\nHere is the LCS matrix for the first sentences from each text:')
for row in lcs_matrix_with_tokens:
    print(format_row.format(*row))

plagiarism_threshold = 0.1
lcs_lengths_list = []
print('\nHere is the LCS length for every pair of sentences:')
for i in range(len(second_text)):
    lcs_length = main.find_lcs_length(first_text[i], second_text[i], plagiarism_threshold)
    lcs_lengths_list.append(lcs_length)
    print(f'{i + 1}) {lcs_length}')

lcs = main.find_lcs(first_text[0], second_text[0], lcs_matrix)
print(f'\nHere is the LCS itself for the first sentences from each text:\n{lcs}')

print('\nHere is the plagiarism score for every sentence from the second text:')
for i in range(len(second_text)):
    p_score = main.calculate_plagiarism_score(lcs_lengths_list[i], second_text[i])
    print(f'{i+1}) {p_score}')

text_p_score = main.calculate_text_plagiarism_score(first_text, second_text, plagiarism_threshold = 0.1)
print(f'\nHere is the plagiarism score for the whole second text:\n{text_p_score}')

accumulated_diff_stats = main.accumulate_diff_stats(first_text, second_text, plagiarism_threshold = 0.1)
report = main.create_diff_report(first_text, second_text, accumulated_diff_stats)
print(f'\nHere is the report:\n{report}')

RESULT = report
assert RESULT == '''- i have a | cat |
+ i have a | lizard |

lcs = 3, plagiarism = 75.0%

- | it | has | eight limbs |
+ | he | has | a long tail |

lcs = 1, plagiarism = 20.0%

- | its | name is | octocat |
+ | his | name is | mister lizard |

lcs = 2, plagiarism = 40.0%

Text average plagiarism (words): 45.0%''', 'Not working'
