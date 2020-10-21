"""
Longest common subsequence implementation starter
"""

import copy
import main

FIRST_TEXT = '''I have a cat.
It has eight limbs.
Its name is Octocat.'''

SECOND_TEXT = '''I have a lizard.
He has a long tail.
His name is Mister Lizard.'''

FIRST_TEXT = main.tokenize_by_lines(FIRST_TEXT)
SECOND_TEXT = main.tokenize_by_lines(SECOND_TEXT)
print(f'Here are the tokens for each text:\n{FIRST_TEXT}\n{SECOND_TEXT}')

lcs_matrix = main.fill_lcs_matrix(FIRST_TEXT[0], SECOND_TEXT[0])
lcs_matrix_with_tokens = copy.deepcopy(lcs_matrix)
lcs_matrix_with_tokens.insert(0, list(SECOND_TEXT[0]))
lcs_matrix_with_tokens[0].insert(0, 0)
for i in range(1, len(lcs_matrix_with_tokens)):
    lcs_matrix_with_tokens[i].insert(0, FIRST_TEXT[0][i-1])
format_row = '{:<5}' * len(lcs_matrix_with_tokens[0])
print('\nHere is the LCS matrix for the first sentences from each text:')
for row in lcs_matrix_with_tokens:
    print(format_row.format(*row))

PLAGIARISM_THRESHOLD = 0.1
lcs_lengths_list = []
print('\nHere is the LCS length for every pair of sentences:')
for i, sentence in enumerate(SECOND_TEXT):
    LCS_LENGTH = main.find_lcs_length(FIRST_TEXT[i], sentence, PLAGIARISM_THRESHOLD)
    lcs_lengths_list.append(LCS_LENGTH)
    print(f'{i + 1}) {LCS_LENGTH}')

lcs = main.find_lcs(FIRST_TEXT[0], SECOND_TEXT[0], lcs_matrix)
print(f'\nHere is the LCS itself for the first sentences from each text:\n{lcs}')

print('\nHere is the plagiarism score for every sentence from the second text:')
for i, sentence in enumerate(SECOND_TEXT):
    p_score = main.calculate_plagiarism_score(lcs_lengths_list[i], sentence)
    print(f'{i+1}) {p_score}')

text_p_score = main.calculate_text_plagiarism_score(FIRST_TEXT, SECOND_TEXT, plagiarism_threshold = 0.1)
print(f'\nHere is the plagiarism score for the whole second text:\n{text_p_score}')

accumulated_diff_stats = main.accumulate_diff_stats(FIRST_TEXT, SECOND_TEXT, plagiarism_threshold = 0.1)
report = main.create_diff_report(FIRST_TEXT, SECOND_TEXT, accumulated_diff_stats)
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
