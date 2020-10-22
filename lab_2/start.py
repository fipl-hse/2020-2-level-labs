"""
Longest common subsequence implementation starter
"""
from main import tokenize_by_lines
from main import create_zero_matrix
from main import fill_lcs_matrix
from main import find_lcs_length
from main import find_lcs
from main import calculate_plagiarism_score
from main import calculate_text_plagiarism_score

text1 = 'I have a cat.'
text2 = 'I have a cat.'

tokenized_text1 = tokenize_by_lines(text1)
print('Кортеж предложений с токенами из текста 1:', tokenized_text1)
tokenized_text2 = tokenize_by_lines(text2)
print('Кортеж предложений с токенами из текста 2: ', tokenized_text2)

original = tokenized_text1[0]
suspicious = tokenized_text2[0]

zero_matrix = create_zero_matrix(len(original), len(suspicious))
print('Нулевая матрица: ')
for i in range(len(zero_matrix)):
    for j in range(len(zero_matrix[0])):
        print(zero_matrix[i][j], end=' ')
    print()

lcs_matrix = fill_lcs_matrix(original, suspicious)
print('Longest common subsequence matrix: ')
for i in range(len(lcs_matrix)):
    for j in range(len(lcs_matrix[0])):
        print(lcs_matrix[i][j], end=' ')
    print()

length = find_lcs_length(original, suspicious, 0.3)
print('Длина наибольшей общей подпоследовательности: ', length)

lcs = find_lcs(original, suspicious, lcs_matrix)
print('Наибольшая общая подпоследовательность: ', lcs)

plagiarism_score = calculate_plagiarism_score(length, suspicious)
print('Количество плагиата: ', plagiarism_score)

score = calculate_text_plagiarism_score(tokenized_text1, tokenized_text2, 0.3)
print(score)

expected = ('i', 'have', 'a', 'cat')
actual = find_lcs(original, suspicious, lcs_matrix)
RESULT = actual
# DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
assert RESULT == expected, 'Program works wrong'
