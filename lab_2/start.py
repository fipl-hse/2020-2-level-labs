"""
Longest common subsequence implementation starter
"""

import main


if __name__ == '__main__':
    original_text_tokens = (('i', 'have', 'a', 'cat'),
                            ('its', 'body', 'is', 'covered', 'with', 'bushy', 'white', 'fur'))
    # nothing
    suspicious_text_tokens = (('i', 'have', 'a', 'cat'),
                              ('its', 'body', 'is', 'covered', 'with', 'shiny', 'black', 'fur'))

RESULT = main.create_diff_report
assert RESULT
