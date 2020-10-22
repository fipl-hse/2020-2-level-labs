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

text1 = 'Once upon a time there lived a cat named Mary.'
text2 = 'Not a long time ago there lived an owl named Rena.'

tokenized_text1 = tokenize(text1)
print('Кортеж предложений с токенами из текста 1:', tokenized_text1)
tokenized_text2 = tokenize(text2)
print('Кортеж предложений с токенами из текста 2: ', tokenized_text2)

zero_matrix = create_zero_matrix(len(tokenized_text1), len(tokenized_text2))
print('Матрица из нулей: ')
for i in range(len(zero_matrix)):
    for j in range(len(zero_matrix[0])):
        print(zero_matrix[i][j], end=' ')
    print()

lcs_matrix = fill_lcs_matrix(tokenized_text1, tokenized_text2)
print('Longest common subsequence matrix: ', lcs_matrix)
for i in range(len(lcs_matrix)):
    for j in range(len(lcs_matrix[0])):
        print(lcs_matrix[i][j], end=' ')
    print()

length = find_lcs_length(tokenized_text1, tokenized_text2, 0.3)
print('Length of the longest common subsequence: ', length)

lcs = find_lcs(tokenized_text1, tokenized_text2, lcs_matrix)
print('The longest common subsequence itself: ', lcs)

plagiarism_score = calculate_plagiarism_score(length, tokenized_text2)
print('the plagiarism score: ', plagiarism_score)

score = calculate_text_plagiarism_score(tokenized_text1, tokenized_text2, 0.3)
print(score)
