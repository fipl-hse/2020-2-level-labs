"""
Language detector implementation starter
"""

import lab_3.main
if __name__ == '__main__':

    # here goes your function calls
    file_english = open('Frank_Baum.txt', encoding='utf-8')
    file_german = open('Thomas_Mann.txt', encoding='utf-8')
    file_unknown = open('unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')

    text_english = lab_3.main.tokenize_by_sentence(file_english.read())
    text_german = lab_3.main.tokenize_by_sentence(file_german.read())
    text_unknown = lab_3.main.tokenize_by_sentence(file_unknown.read())

    file_english.close()
    file_german.close()
    file_unknown.close()

    letter_storage = lab_3.main.LetterStorage()
    letter_storage.update(text_english)
    letter_storage.update(text_german)
    letter_storage.update(text_unknown)

    encoded_english = lab_3.main.encode_corpus(letter_storage, text_english)
    encoded_german = lab_3.main.encode_corpus(letter_storage, text_german)
    encoded_unknown = lab_3.main.encode_corpus(letter_storage, text_unknown)

    language_detector = lab_3.main.LanguageDetector((2,3), 100)
    language_detector.new_language(encoded_english, 'english')
    language_detector.new_language(encoded_german, 'german')

    detected_language = language_detector.detect_language(encoded_unknown)
    if detected_language['english'] > detected_language['german']:
        RESULT = 'english'
    else:
        RESULT = 'german'

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == 'german', 'detector is not working'
