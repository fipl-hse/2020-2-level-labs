"""
Longest common subsequence implementation starter
"""
import main

if __name__ == '__main__':
    ORIGINAL_TEXT = 'I have a dog.\nHis name is Tom.\n I bought it yesterday.'
    SUSPICIOUS_TEXT = 'I have a cat.\nHer name is Mary.\nI found her today.'

    tokenized_orig_text = main.tokenize_by_lines(ORIGINAL_TEXT)
    tokenized_susp_text = main.tokenize_by_lines(SUSPICIOUS_TEXT)
    print(f"Original text tokens: {tokenized_orig_text}\nSuspicious text tokens: {tokenized_susp_text}\n")

    orig_first_sent = tokenized_orig_text[2]
    susp_first_sent = tokenized_susp_text[2]

    zero_matrix_first = main.create_zero_matrix(len(orig_first_sent), len(susp_first_sent))
    lcs_matrix = main.fill_lcs_matrix(orig_first_sent, susp_first_sent)
    print(f"Filled LCS matrix for first sentences: {lcs_matrix}\n")

    lcs_length = main.find_lcs_length(orig_first_sent, susp_first_sent, 0.3)
    print(f"LCS length for first sentences: {lcs_length}\n")

    lcs = main.find_lcs(orig_first_sent, susp_first_sent, lcs_matrix)
    print(f"LCS for first sentences: {lcs}\n")

    plagiarism_score = main.calculate_plagiarism_score(lcs_length, susp_first_sent)
    print(f"The plagiarism score for first sentences: {plagiarism_score}\n")

    plagiarism_text = main.calculate_text_plagiarism_score(tokenized_orig_text, tokenized_susp_text,
                                                           plagiarism_threshold=0.3)
    print(f"The plagiarism score for the text: {plagiarism_text}\n")

    diff_in_sent = main.find_diff_in_sentence(orig_first_sent, susp_first_sent, lcs)
    print(f"Indexes of differences in first sentences: {diff_in_sent}\n")

    statistics = main.accumulate_diff_stats(tokenized_orig_text, tokenized_susp_text, plagiarism_threshold=0.3)
    print(f"The main statistics for pairs of sentences in texts:\n{statistics}\n")

    report = main.create_diff_report(tokenized_orig_text, tokenized_susp_text, statistics)
    print(f"The report for two texts:\n{report}")

    RESULT = report.split('\n')

    assert RESULT == ['- i have a | dog |', '+ i have a | cat |',
                      'lcs = 3, plagiarism = 75.0%', ' ',
                      '- | his | name is | tom |', '+ | her | name is | mary |',
                      'lcs = 2, plagiarism = 50.0%', ' ',
                      '- i | bought it yesterday |', '+ i | found her today |',
                      'lcs = 0, plagiarism = 0.0%', ' ',
                      'Text average plagiarism(words): 41.66666666666667%'], 'LCS not working'
