"""
Longest common subsequence implementation starter
"""
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
assert RESULT == expected, 'Concordance not working'

