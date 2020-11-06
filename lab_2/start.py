"""
Longest common subsequence implementation starter
"""
from main import tokenize_by_lines, accumulate_diff_stats, create_diff_report

TEXT_ORIGINAL = '''This is the horse and the hound and the horn.
That belonged to the farmer sowing his corn.
That kept the cock that crowed in the morn.
That waked the priest all shaven and shorn.
That married the man all tattered and torn.
That kissed the maiden all forlorn.
That milked the cow with the crumpled horn.
That tossed the dog that worried the cat.
That killed the rat that ate the malt.
That lay in the house that Jack built.'''

TEXT_SUSPICIOUS = '''This is the cow and the raccoon and the horn.
That kept the chicken that crowed in the morn!
That waked the priest all shaven and shorn!
That belonged to the farmer sowing his corn.
hat married the man all tattered and torn!
That kissed the woman all forlorn?
That milked the goat with the crumpled horn.
That killed the rat that ate the malt.
That tossed the dog that worried the cat.
That stay in the house that Jack built.'''

original_tuple = tokenize_by_lines(TEXT_ORIGINAL)
suspicious_tuple = tokenize_by_lines(TEXT_SUSPICIOUS)

diff_stats = accumulate_diff_stats(original_tuple, suspicious_tuple)

RESULT = create_diff_report(original_tuple, suspicious_tuple, diff_stats)

assert RESULT, 'LCS_length not working'