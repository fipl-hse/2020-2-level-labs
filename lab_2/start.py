"""
Longest common subsequence implementation starter
"""
import main

if __name__ == '__main__':
    ORIGINAL_TEXT = 'The dog is walking.\nThe cat is sleeping.\nThe boy has a cat.\nThe girl has a dog.'
    SUSPICIOUS_TEXT = 'Mike is running.\nAnna is sleeping.\nMary has a cat.\nJack has a cat.'

    original_text_tuple = main.tokenize_by_lines(ORIGINAL_TEXT)
    suspicious_text_tuple = main.tokenize_by_lines(SUSPICIOUS_TEXT)

    print('Original text: {}\n'.format(original_text_tuple, suspicious_text_tuple))

    ORIGINAL_SENTENCE = original_text_tuple[1]
    SUSPICIOUS_SENTENCE = suspicious_text_tuple[1]
    print('Original sentence: {}\nSuspicious sentence: {}\n'.format(ORIGINAL_SENTENCE, SUSPICIOUS_SENTENCE))

    new_matrix = main.create_zero_matrix(len(ORIGINAL_SENTENCE), len(SUSPICIOUS_SENTENCE))
    print('Zero matrix: {}\n'.format(new_matrix))

    matrix = main.fill_lcs_matrix(ORIGINAL_SENTENCE, SUSPICIOUS_SENTENCE)
    print('Lcs matrix: {}\n'.format(matrix))

    length = main.find_lcs_length(ORIGINAL_SENTENCE, SUSPICIOUS_SENTENCE, 0.3)
    print('Lcs length: {}\n'.format(length))

    lcs = main.find_lcs(ORIGINAL_SENTENCE, SUSPICIOUS_SENTENCE, matrix)
    print('Lcs: {}\n'.format(lcs))

    score = main.calculate_plagiarism_score(length, SUSPICIOUS_SENTENCE)
    print('Plagiarism score: {}\n'.format(score))

    RESULT = find.lcs.length(ORIGINAL_SENTENCE, SUSPICIOUS_SENTENCE, 0.3)
    assert RESULT, 'Lcs length not working'


