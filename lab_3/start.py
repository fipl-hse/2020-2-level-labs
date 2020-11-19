"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls
    unknown_file = open('unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')
    german_file = open('Thomas_Mann.txt', encoding='utf-8')
    english_file = open('Frank_Baum.txt', encoding='utf-8')

    text_unknown = lab_3.main.tokenize_by_sentence(unknown_file.read())
    text_german = lab_3.main.tokenize_by_sentence(german_file.read())
    text_english = lab_3.main.tokenize_by_sentence(english_file.read())
    english_file.close()
    german_file.close()
    unknown_file.close()

    letter_storage = lab_3.main.LetterStorage()
    letter_storage.update(text_unknown)
    letter_storage.update(text_german)
    letter_storage.update(text_english)

    encoded_unknown = lab_3.main.encode_corpus(letter_storage, text_unknown)
    encoded_german = lab_3.main.encode_corpus(letter_storage, text_german)
    encoded_english = lab_3.main.encode_corpus(letter_storage, text_english)

    language_detector = lab_3.main.LanguageDetector((3, 4, 5), 500)
    language_detector.new_language(encoded_english, "english")
    language_detector.new_language(encoded_german, "german")

    language = language_detector.detect_language(encoded_unknown)
    if language["german"] > language["english"]:
        RESULT = "english"
    else:
        RESULT = "german"
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == "german", "Not working"
