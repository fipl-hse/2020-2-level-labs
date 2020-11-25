"""
Language detector implementation starter
"""

from lab_3.main import tokenize_by_sentence, LanguageDetector
from lab_3.main import encode_corpus
from lab_3.main import LetterStorage


if __name__ == '__main__':

    # here goes your function calls
    letter_storage = LetterStorage()
    language_detector = LanguageDetector((3,), 100)

    file_first = open('lab_3/Frank_Baum.txt', 'r', encoding='utf-8')
    file_second = open('lab_3/Thomas_Mann.txt', 'r', encoding='utf-8')
    file_third = open('lab_3/unknown_Arthur_Conan_Doyle.txt', 'r', encoding='utf-8')

    text_english = tokenize_by_sentence(file_first.read())
    text_german = tokenize_by_sentence(file_second.read())
    text_unknown = tokenize_by_sentence(file_third.read())
    letter_storage.update(text_english)
    letter_storage.update(text_german)
    letter_storage.update(text_unknown)
    encoded_english = encode_corpus(letter_storage, text_english)
    encoded_german = encode_corpus(letter_storage, text_german)
    encoded_unknown = encode_corpus(letter_storage, text_unknown)
    file_first.close()
    file_second.close()
    file_third.close()

    language_detector.new_language(encoded_english, 'english')
    language_detector.new_language(encoded_german, 'german')

    actual = language_detector.detect_language(encoded_unknown)
    RESULT = actual['german'] > actual['english']
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == 1, ''
