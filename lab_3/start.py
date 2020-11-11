"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls
    TEXT = 'She is happy. He is happy.'

    RESULT = lab_3.main.tokenize_by_sentence(text)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Nothing works'
