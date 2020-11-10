"""
Longest common subsequence implementation starter
"""
<<<<<<< HEAD
from lab_2 import main
text_sentences_tokenize = main.tokenize_by_lines('I have a cat.\nHis name is Bruno')
print(text_sentences_tokenize)
zero_matrix = main.create_zero_matrix(4, 4)
print(zero_matrix)
lcs_matrix = main.fill_lcs_matrix(('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
print(lcs_matrix)
lcs_length = main.find_lcs_length(('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'), 0.3)
print(lcs_length)
lcs = main.find_lcs(('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'), lcs_matrix)
print(lcs)
plagiarism_score = main.calculate_plagiarism_score(lcs_length, ('his', 'name', 'is', 'bruno'))
print(plagiarism_score)
text_plagiarism_score = main.calculate_text_plagiarism_score((('i', 'have', 'a', 'cat'),
                                                              ('his', 'name', 'is', 'bruno')),
                                                             (('i', 'have', 'a', 'cat'),
                                                              ('his', 'name', 'is', 'paw')), 0.3)
print(text_plagiarism_score)
diff_in_sentence = main.find_diff_in_sentence(('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'), lcs)
print(diff_in_sentence)
diff_stats = main.accumulate_diff_stats((('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno')),
                                        (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'paw')))
print(diff_stats)
diff_report = main.create_diff_report((('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno')),
                                      (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'paw')), diff_stats)
print(diff_report)
RESULT = diff_report
assert RESULT, 'Program not working'
=======
import lab_2.main

if __name__ == '__main__':
    original_text_tokens = (('i', 'have', 'a', 'cat'),
                            ('its', 'body', 'is', 'covered', 'with', 'bushy', 'white', 'fur'))
    suspicious_text_tokens = (('i', 'have', 'a', 'cat'),
                              ('its', 'body', 'is', 'covered', 'with', 'shiny', 'black', 'fur'))
    accumulated_diff_stats = lab_2.main.accumulate_diff_stats(original_text_tokens, suspicious_text_tokens)

    expected = open('lab_2/diff_report_example.txt', 'r', errors='coerce').read().split()
    actual = lab_2.main.create_diff_report(original_text_tokens, suspicious_text_tokens, accumulated_diff_stats).split()

    RESULT = actual
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == expected, 'Results differ'
>>>>>>> upstream/master
