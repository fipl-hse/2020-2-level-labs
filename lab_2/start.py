"""
Longest common subsequence implementation starter
"""
from tokenizer import tokenize
from main import create_zero_matrix
from main import fill_lcs_matrix
from main import find_lcs_length
from main import find_lcs
from main import calculate_plagiarism_score
from main import calculate_text_plagiarism_score
from main import find_diff_in_sentence
from main import accumulate_diff_stats
from main import create_diff_report
from main import find_lcs_length_optimized

with open('text1.txt', 'r') as report:
    data1 = report.read()
print(data1)

with open('text2.txt', 'r') as report:
    data2 = report.read()
print(data2)

tokenized_text1 = tokenize(data1)
# tokenized_text2 = tokenize(data2)
print('Кортеж предложений с токенами:', tokenized_text1)
# print('Кортеж предложений с токенами: ', tokenized_text2)

zero_matrix = create_zero_matrix(2,5)
print()
print(zero_matrix)

lcs_matrix = fill_lcs_matrix(data1, data2)
print(lcs_matrix)