"""
Longest common subsequence implementation starter
"""
import main

if __name__ == '__main__':
    original_text = 'The weather is sunny.\nI am going to meet my friend Liza.\n' \
                    'She is very nice, smart and funny.'
    suspicious_text = 'The weather is bad.\nI am going to meet my brother Nikita.\n' \
                      'He is very nice, clever and funny.'
    processed_text_orig = main.tokenize_by_lines(original_text)
    processed_text_sus = main.tokenize_by_lines(suspicious_text)
    print(f"Original text tokens: {processed_text_orig}\nSuspicious text tokens: {processed_text_sus}")

    sentence_orig = processed_text_orig[1]
    sentence_sus = processed_text_sus[1]

    zero_matrix = main.create_zero_matrix(len(sentence_orig), len(sentence_sus))
    print(f'Zero matrix: {zero_matrix}')

    lcs_matrix = main.fill_lcs_matrix(sentence_orig, sentence_sus)
    print(f"Filled LCS matrix: {lcs_matrix}")

    lcs_length = main.find_lcs_length(sentence_orig, sentence_sus, 0.3)
    print(f'LCS length: {lcs_length}')

    lcs = main.find_lcs(sentence_orig, sentence_sus, lcs_matrix)
    print(f'LCS: {lcs}')

    plagiarism_score = main.calculate_plagiarism_score(lcs_length, sentence_sus)
    print(f'Plagiarism score: {plagiarism_score}')

    text_plagiarism_score = main.calculate_text_plagiarism_score(processed_text_orig, processed_text_sus,
                                                                 plagiarism_threshold=0.3)
    print(f'Text plagiarism score: {text_plagiarism_score}')

    different_indexes = main.find_diff_in_sentence(sentence_orig, sentence_sus, lcs)
    print(f'Indexes of different words in sentences: {different_indexes}')

    statistics = main.accumulate_diff_stats(processed_text_orig, processed_text_sus, plagiarism_threshold=0.3)
    print(f'Statistics: {statistics}')

    plagiarism_report = main.create_diff_report(processed_text_orig, processed_text_sus, statistics)
    print(f'Plagiarism report:\n{plagiarism_report}')

    RESULT = plagiarism_report.split("\n")
    assert RESULT, 'LCS not working'




