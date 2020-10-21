"""
Longest common subsequence implementation starter
"""

import os
import main

if __name__ == '__main__':
    text = 'I have a cat.\nHis name is Bruno'
    tokenizer = main.tokenize_by_lines(text)
    print(tokenizer)

    zero_matrix = main.create_zero_matrix(2, 2)
    print(zero_matrix)

    fill_lcs = main.fill_lcs_matrix(('the', 'dog', 'is', 'running'), ('the', 'cat', 'is', 'sleeping'))
    print(fill_lcs)

    lcs_length = main.find_lcs_length(('the', 'dog', 'is', 'running'), ('the', 'cat', 'is', 'sleeping'), 0.3)
    print(lcs_length)

    lcs_matrix = [[1, 1, 1, 1],
                  [1, 1, 1, 1],
                  [1, 1, 2, 2],
                  [1, 1, 2, 2]]
    lcs = main.find_lcs(('the', 'dog', 'is', 'running'), ('the', 'cat', 'is', 'sleeping'), lcs_matrix)
    print(lcs)

    plagiarism_sent = main.calculate_plagiarism_score(3, ('the', 'cat', 'is', 'sleeping'))
    print(plagiarism_sent)

    sentence = (('the', 'cat', 'left'),
                ('the', 'dog', 'disappeared'))
    plagiarism_text = main.calculate_text_plagiarism_score(sentence, sentence, 0.3)
    print(plagiarism_text)

    RESULT = plagiarism_sent
    assert RESULT == 0.75, 'lcs not working'