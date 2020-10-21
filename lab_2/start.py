"""
Longest common subsequence implementation starter
"""

import main

if __name__ == '__main__':
    ORIGINAL_TEXT = 'I have a dog.\nHis name is Nemo.\nI found him yesterday'
    SUSPICIOUS_TEXT = 'I have a cat.\nHer name is Anny.\nI met her yesterday'

    original_text_tuple = main.tokenize_by_lines(ORIGINAL_TEXT)
    suspicious_text_tuple = main.tokenize_by_lines(SUSPICIOUS_TEXT)

    print('Original text: {}\nSuspicious text: {}\n'.format(original_text_tuple, suspicious_text_tuple))

    ORIGINAL_SENTENCE = original_text_tuple[1]
    SUSPICIOUS_SENTENCE = suspicious_text_tuple[1]
    print('Original sentence: {}\nSuspicious sentence: {}\n'.format(ORIGINAL_SENTENCE, SUSPICIOUS_SENTENCE))

    zero_matrix = main.create_zero_matrix(len(ORIGINAL_SENTENCE), len(SUSPICIOUS_SENTENCE))
    print('Zero matrix: {}\n'.format(zero_matrix))

    lcs_matrix = main.fill_lcs_matrix(ORIGINAL_SENTENCE, SUSPICIOUS_SENTENCE)
    print('LCS matrix: {}\n'.format(lcs_matrix))

    lcs_length = main.find_lcs_length(ORIGINAL_SENTENCE, SUSPICIOUS_SENTENCE, 0.3)
    print('LCS length: {}\n'.format(lcs_length))

    lcs = main.find_lcs(ORIGINAL_SENTENCE, SUSPICIOUS_SENTENCE, lcs_matrix)
    print('LCS: {}\n'.format(lcs))

    plagiarism_score = main.calculate_plagiarism_score(lcs_length, SUSPICIOUS_SENTENCE)
    print('Plagiarism score: {}\n'.format(plagiarism_score))

    text_plagiarism_score = main.calculate_text_plagiarism_score(original_text_tuple, suspicious_text_tuple,
                                                                 plagiarism_threshold=0.3)
    print('Text plagiarism score: {}\n'.format(text_plagiarism_score))

    diff_in_sentence = main.find_diff_in_sentence(ORIGINAL_SENTENCE, SUSPICIOUS_SENTENCE, lcs)
    print('Difference-indexes in sentences: {}\n'.format(diff_in_sentence))

    diff_stats = main.accumulate_diff_stats(original_text_tuple, suspicious_text_tuple, plagiarism_threshold=0.3)
    print('Difference-statistics: {}\n'.format(diff_stats))

    diff_report = main.create_diff_report(original_text_tuple, suspicious_text_tuple, diff_stats)
    print('Plagiarism report:\n{}\n'.format(diff_report))

    RESULT = diff_report.split('\n')
    assert RESULT == ['- i have a | dog |','+ i have a | cat |', ''
                      'lcs = 3, plagiarism = 75.0%', ''
                      '- | his name is nemo |','+ | her name is anny |',''
                      'lcs = 2, plagiarism = 50.0%', ''
                      '- i | found him | yesterday','+ i | met her | yesterday',''
                      'lcs = 2, plagiarism = 50.0%', ''
                      'Text average plagiarism (words): 58.333333333333336%'],'LCS not working'