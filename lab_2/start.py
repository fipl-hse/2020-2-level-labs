"""
Longest common subsequence implementation starter
"""
import main

ORIGINAL_TEXT = 'Yes, I have a cat, and his name is Pooh.'
SUSPICIOUS_TEXT = 'No, I have a dog, and I call her Paw.'

original_tokens = main.tokenize_by_lines(ORIGINAL_TEXT)
suspicious_tokens = main.tokenize_by_lines(SUSPICIOUS_TEXT)

print("Tokenized original text:", original_tokens)
print("Tokenized suspicious text:", suspicious_tokens)

original_sentence = original_tokens[0]
suspicious_sentence = suspicious_tokens[0]

matrix = main.fill_lcs_matrix(original_sentence, suspicious_sentence)
print("The lcs matrix:", matrix)

lcs_length = main.find_lcs_length(original_sentence, suspicious_sentence, plagiarism_threshold=0.3)
print("Length of the longest common subsequence:", lcs_length)

lcs = main.find_lcs(original_sentence, suspicious_sentence, matrix)
print("The longest common subsequence:", lcs)

plagiarism_score = main.calculate_plagiarism_score(lcs_length, suspicious_sentence)
print("The plagiarism score:", plagiarism_score)

stat = main.accumulate_diff_stats(original_tokens, suspicious_tokens)
report = main.create_diff_report(original_tokens, suspicious_tokens, stat)
print("The statistics for the whole text:", report)

RESULT = report
assert RESULT == '''- | yes | i have a | cat | and | his name is pooh |
+ | no | i have a | dog | and | i call her paw |

lcs = 4, plagiarism = 40.0%

Text average plagiarism (words): 40.0%''', 'Not working'
