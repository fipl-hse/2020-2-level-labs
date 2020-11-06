"""
Longest common subsequence implementation starter
"""
accumulated_diff_stats = lab_2.main.accumulate_diff_stats(original_text_tokens, suspicious_text_tokens)
expected = open('lab_2/diff_report_example.txt', 'r', errors='coerce').read().split()
#actual = lab_2.main.create_diff_report(original_text_tokens, suspicious_text_tokens, accumulated_diff_stats).split()
#RESULT = actual
# DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
#assert RESULT == expected, 'Results differ'


