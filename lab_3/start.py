"""
Language detector implementation starter
"""

import lab_3.main
from lab_3.main import tokenize_by_sentence
from lab_3.main import LetterStorage

if __name__ == '__main__':

    # here goes your function calls
    unknown_file = open('lab_3/unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')
    german_file = open('lab_3/Thomas_Mann.txt', encoding='utf-8')
    english_file = open('lab_3/Frank_Baum.txt', encoding='utf-8')

    text_unk = tokenize_by_sentence(unknown_file.read())
    text_ger = tokenize_by_sentence(german_file.read())
    text_eng = tokenize_by_sentence(english_file.read())
    english_file.close()
    german_file.close()
    unknown_file.close()

    letter_storage = LetterStorage()
    letter_storage.update(text_eng)
    letter_storage.update(text_ger)
    letter_storage.update(text_unk)

    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, ''
