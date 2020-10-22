"""
Longest common subsequence implementation starter
"""

import main

if __name__ == '__main__':

    PAIR_OF_SENTENCES = 'The weather is sunny and good! //\n The man is happy and satisfied.'
    res_of_tokenize = main.tokenize_by_lines(PAIR_OF_SENTENCES)
    sentence_1 = res_of_tokenize[0]
    sentence_2 = res_of_tokenize[1]
    print('\nFIRST SENTENCE: ', sentence_1, '\n\nSECOND SENTENCE: ', sentence_2)

    lcs_matrix = main.fill_lcs_matrix(sentence_1, sentence_2)
    print('\nLCS MATRIX: ', lcs_matrix)

    lcs_length = main.find_lcs_length(sentence_1, sentence_2, plagiarism_threshold = 0.3)
    print('\nLCS LENGTH: ', lcs_length)

    lcs = main.find_lcs(sentence_1, sentence_2, lcs_matrix)
    print('\nLCS: ', lcs)

    plagiarism_score = main.calculate_plagiarism_score(lcs_length, sentence_2)
    print('\nPLAGIARISM SCORE: ', plagiarism_score)

    RESULT = plagiarism_score
    assert RESULT == 0.5, 'Plagiarism score is not working'
