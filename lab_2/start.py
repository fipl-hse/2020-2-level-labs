"""
Longest common subsequence implementation starter
"""
from main import tokenize_by_lines, accumulate_diff_stats, create_diff_report

TEXT_ORIGINAL = '''i like small cats'''

TEXT_SUSPICIOUS = '''i prefer small dogs'''

original_tuple = tokenize_by_lines(TEXT_ORIGINAL)
suspicious_tuple = tokenize_by_lines(TEXT_SUSPICIOUS)

diff_stats = accumulate_diff_stats(original_tuple, suspicious_tuple)

RESULT = create_diff_report(original_tuple, suspicious_tuple, diff_stats)

assert RESULT, 'LCS_length not working'
