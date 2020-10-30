"""
Longest common subsequence implementation starter
"""
import lab_2.main

ORIGINAL = 'the cat is sleeping'
SUSPICIOUS = 'the little cat is running'

original_tokens = lab2.main.tokenize_by_lines(ORIGINAL)
suspicious_tokens = lab2.main.tokenize_by_lines(SUSPICIOUS)

print("Tokenized original text:", original_tokens)
print("Tokenized suspicious text:", suspicious_tokens)

lcs_length = lab2.main.find_lcs_length(original_tokens, suspicious_tokens, plagiarism_threshold=0.3)
print("Length of the longest common subsequence:", lcs_length)

matrix = lab2.main.fill_lcs_matrix(original_tokens, suspicious_tokens)

lcs = lab2.main.find_lcs(original_tokens, suspicious_tokens, matrix)
print("The longest common subsequence:", lcs)

plagiarism_score = lab2.main.calculate_plagiarism_score(lcs_length, suspicious_tokens)
print("The plagiarism score:", plagiarism_score)

text_plagiarism_score = lab2.main.calculate_text_plagiarism_score(original_tokens, suspicious_tokens, plagiarism_score)
print("Text average plagiarism:", text_plagiarism_score)

RESULT = text_plagiarism_score
assert RESULT, 'Not working'
