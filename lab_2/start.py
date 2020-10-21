"""
Longest common subsequence implementation starter
"""
import main

if __name__ == '__main__':
    ORIGINAL_TEXT = 'The weather is sunny.\nI am going to meet my friend Nikita.\n' \
                    'She is very nice, smart and funny.'
    SUSPICIOUS_TEXT = 'The weather is bad.\nI am going to meet my brother Nikita.\n' \
                      'He is very nice, clever and funny.'
    processed_text_orig = main.tokenize_by_lines(ORIGINAL_TEXT)
    processed_text_sus = main.tokenize_by_lines(SUSPICIOUS_TEXT)
    print(f"Original text tokens: {processed_text_orig}\nSuspicious text tokens: {processed_text_sus}\n")

    sentence_orig = processed_text_orig[1]
    sentence_sus = processed_text_sus[1]

    zero_matrix = main.create_zero_matrix(len(sentence_orig), len(sentence_sus))
    print(f'Zero matrix: {zero_matrix}\n')

    lcs_matrix = main.fill_lcs_matrix(sentence_orig, sentence_sus)
    print(f"Filled LCS matrix: {lcs_matrix}\n")

    lcs_length = main.find_lcs_length(sentence_orig, sentence_sus, 0.3)
    print(f'LCS length: {lcs_length}\n')

    lcs = main.find_lcs(sentence_orig, sentence_sus, lcs_matrix)
    print(f'LCS: {lcs}\n')

    plagiarism_score = main.calculate_plagiarism_score(lcs_length, sentence_sus)
    print(f'Plagiarism score: {plagiarism_score}\n')

    text_plagiarism_score = main.calculate_text_plagiarism_score(processed_text_orig, processed_text_sus,
                                                                 plagiarism_threshold=0.3)
    print(f'Text plagiarism score: {text_plagiarism_score}\n')

    different_indexes = main.find_diff_in_sentence(sentence_orig, sentence_sus, lcs)
    print(f'Indexes of different words in sentences: {different_indexes}\n')

    statistics = main.accumulate_diff_stats(processed_text_orig, processed_text_sus, plagiarism_threshold=0.3)
    print(f'Statistics:\n{statistics}\n')

    plagiarism_report = main.create_diff_report(processed_text_orig, processed_text_sus, statistics)
    print(f'Plagiarism report:\n{plagiarism_report}')

    RESULT = plagiarism_report.split("\n")
    assert RESULT == ['- the weather is | sunny ', '+ the weather is | bad ', '',
                      'lcs = 3, plagiarism = 75.0%', '', '- i am going to meet my | friend | nikita ',
                      '+ i am going to meet my | brother | nikita ', '', 'lcs = 7, plagiarism = 87.5%',
                      '', '- | she | is very nice | smart | and funny ', '+ | he | is very nice | clever | and funny ',
                      '', 'lcs = 5, plagiarism = 71.42857142857143%', '',
                      'Text average plagiarism (words): 77.97619047619048%'], 'LCS not working'


