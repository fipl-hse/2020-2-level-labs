"""
Longest common subsequence implementation starter
"""

import main


if __name__ == '__main__':
    original_text = 'The cat appeared.\nThe dog disappeared.\nHis name is Mike.\nHe has a dog.'
    suspicious_text = 'The man arrived.\nThe boy disappeared.\nHer name is Jane.\nShe has a cat.'

    original_text_tuple = main.tokenize_by_lines(original_text)
    suspicious_text_tuple = main.tokenize_by_lines(suspicious_text)

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
    print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert ['- the | cat appeared |', '+ the | man arrived |', '',
            'lcs = 1, plagiarism = 33.33333333333333%', '',
            '- the | dog | disappeared', '+ the | boy | disappeared', '',
            'lcs = 2, plagiarism = 66.66666666666666%', '',
            '- | his name is mike |', '+ | her name is jane |', '',
            'lcs = 2, plagiarism = 50.0%', '',
            '- | he has a dog |', '+ | she has a cat |', '',
            'lcs = 2, plagiarism = 50.0%', '',
            'Text average plagiarism (words): 50.0%'], 'LCS not working'
