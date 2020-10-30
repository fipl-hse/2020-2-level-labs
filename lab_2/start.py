"""
Longest common subsequence implementation starter
"""

from main import tokenize_by_lines, accumulate_diff_stats, create_diff_report

ORIGINAL_TEXT = "i like small cats"

SUSPICIOUS_TEXT = "i prefer small dogs"

original = tokenize_by_lines(ORIGINAL_TEXT)
suspicious = tokenize_by_lines(SUSPICIOUS_TEXT)

diff_stats = accumulate_diff_stats(original, suspicious)

RESULT = create_diff_report(original, suspicious, diff_stats)
assert RESULT, "LCS_length not working"
