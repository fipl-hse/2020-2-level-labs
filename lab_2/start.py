"""
Longest common subsequence implementation starter
"""
import lab_2.main


if __name__ == '__main__':
    '''original_text_tokens = (('i', 'have', 'a', 'cat'),
                            ('its', 'body', 'is', 'covered', 'with', 'bushy', 'white', 'fur'))
    suspicious_text_tokens = (('i', 'have', 'a', 'cat'),
                              ('its', 'body', 'is', 'covered', 'with', 'shiny', 'black', 'fur'))
    accumulated_diff_stats = lab_2.main.accumulate_diff_stats(original_text_tokens, suspicious_text_tokens)

    expected = open('lab_2/diff_report_example.txt', 'r', errors='coerce').read().split()
    actual = lab_2.main.create_diff_report(original_text_tokens, 
                                           suspicious_text_tokens, accumulated_diff_stats).split()'''

    sentence_tokens_first_text = lab_2.main.tokenize_big_file('lab_2/data.txt')[:20000]
    sentence_tokens_second_text = lab_2.main.tokenize_big_file('lab_2/data_2.txt')[:20000]
    plagiarism_threshold = 0.0001
    lcs_length = lab_2.main.find_lcs_length_optimized(sentence_tokens_first_text,
                                                      sentence_tokens_second_text,
                                                      plagiarism_threshold)
    actual = lcs_length / len(sentence_tokens_second_text)
    expected = 2580 / 20000
    RESULT = actual
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == expected, 'Results differ'
