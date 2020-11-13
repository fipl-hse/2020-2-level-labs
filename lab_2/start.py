"""
Longest common subsequence implementation starter
"""
<<<<<<< HEAD
import main


if __name__ == '__main__':
    original_tokens = main.tokenize_big_file('lab_2/data.txt'[:3000])
    suspicious_tokens = main.tokenize_big_file('lab_2/data_2.txt'[:3000])
    lcs_length = main.find_lcs_length_optimized(original_tokens, suspicious_tokens, 0.0001)
    print('Longest common subsequence consists of {} words.'.format(lcs_length))
    actual = main.calculate_plagiarism_score(lcs_length, suspicious_tokens)
    print('The ratio of borrowings from the first text in the second text is {}'.format(actual))
    RESULT = 60 / 502

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Calculation of text plagiarism is not working'
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
>>>>>>> cd2909df66a6e74a9c6263dfcf079164a12bfdd3
