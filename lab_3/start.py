"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls

    english_file = open('lab_3/Frank_Baum.txt', encoding='utf-8')
    german_file = open('lab_3/Thomas_Mann.txt', encoding='utf-8')
    unknown_file = open('lab_3/unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')

    english_text = lab_3.main.tokenize_by_sentence(english_file.read())
    german_text = lab_3.main.tokenize_by_sentence(german_file.read())
    unknown_text = lab_3.main.tokenize_by_sentence(unknown_file.read())

    english_file.close()
    german_file.close()
    unknown_file.close()

    letter_storage = lab_3.main.LetterStorage()
    letter_storage.update(english_text)
    letter_storage.update(german_text)
    letter_storage.update(unknown_text)

    encoded_english = lab_3.main.encode_corpus(letter_storage, english_text)
    encoded_german = lab_3.main.encode_corpus(letter_storage, german_text)
    encoded_unknown = lab_3.main.encode_corpus(letter_storage, unknown_text)

    language_detector = lab_3.main.ProbabilityLanguageDetector((3, 4, 5), 1000)
    language_detector.new_language(encoded_english, 'english')
    language_detector.new_language(encoded_german, 'german')

    ngram_unknown = lab_3.main.NGramTrie(4)
    ngram_unknown.fill_n_grams(encoded_unknown)

    actual = language_detector.detect_language(ngram_unknown.n_grams)

    RESULT = actual['german'] > actual['english']
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == 1, ''
