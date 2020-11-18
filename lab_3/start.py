"""
Language detector implementation starter
"""

from lab_3.main import tokenize_by_sentence
from lab_3.main import encode_corpus
from lab_3.main import NGramTrie
from lab_3.main import LetterStorage
from lab_3.main import LanguageDetector

if __name__ == '__main__':

    # here goes your function calls
    unknown_file = open('lab_3/unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')
    german_file = open('lab_3/Thomas_Mann.txt', encoding='utf-8')
    english_file = open('lab_3/Frank_baum.txt', encoding='utf-8')

    unknown_text = tokenize_by_sentence(unknown_file.read())
    german_text = tokenize_by_sentence(german_file.read())
    english_text = tokenize_by_sentence(english_file.read())
    unknown_file.close()
    german_file.close()
    english_file.close()

    letter_storage = LetterStorage()
    letter_storage.update(english_text)
    letter_storage.update(german_text)
    letter_storage.update(unknown_text)

    english_encoded_text = encode_corpus(letter_storage, english_text)
    german_encoded_text = encode_corpus(letter_storage, german_text)
    unknown_encoded_text = encode_corpus(letter_storage, unknown_text)

    language_detector = LanguageDetector((3, 4, 5), 1000)
    language_detector.new_language(english_encoded_text, 'english')
    language_detector.new_language(german_encoded_text, 'german')

    unknown_n_gram = NGramTrie(4)
    unknown_n_gram.fill_n_grams(unknown_encoded_text)

    actual = language_detector.detect_language(unknown_n_gram.n_grams)
    print(actual)

    RESULT = actual['english'] < actual['german']
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == 1, ''
