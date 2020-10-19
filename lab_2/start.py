"""
Longest common subsequence implementation starter
"""

import main
from tokenizer import tokenize


if __name__ == "__main__":
        origin_text = 'the big cat is sleeping'
    susp_text = 'the cat is big'

    origin_tokens = tokenize(origin_text)
    susp_tokens = tokenize(susp_text)

    print(f'Raw text: {origin_text}')
    print(f'Tokenized text: {origin_tokens}\n\n')

    lcs_lenght = main.find_lcs_length(origin_tokens,
                                      susp_tokens,
                                      plagiarism_threshold=0.0)
    print('A length of the longest common subsequence for \n\n'
        f'{origin_text} \n\n'
        f'and \n\n'
        f'{susp_text}: \n\n'
        f'{lcs_lenght} \n')

    matrix = main.fill_lcs_matrix(origin_tokens, susp_tokens)
    print(f'A matrix:')
    print(*matrix, sep='\n', end='\n\n')

    longest_lcs = main.find_lcs(origin_tokens, susp_tokens, matrix)
    print(f'The longest common subsequence: {longest_lcs}')

    score = main.calculate_plagiarism_score(lcs_lenght, susp_tokens)
    print(f'The plagiarism score: {score:.2f}\n')
    
    RESULT = score
    assert RESULT, 'Plagiarism checker not working'