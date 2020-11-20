"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls

    unknown_file = open('lab_3/unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')
    german_file = open('lab_3/Thomas_Mann.txt', encoding='utf-8')
    english_file = open('lab_3/Frank_Baum.txt', encoding='utf-8')

    text_unk = lab_3.main.tokenize_by_sentence(unknown_file.read())
    text_ger = lab_3.main.tokenize_by_sentence(german_file.read())
    text_eng = lab_3.main.tokenize_by_sentence(english_file.read())
    english_file.close()
    german_file.close()
    unknown_file.close()

    letter_storage = lab_3.main.LetterStorage()
    letter_storage.update(text_eng)
    letter_storage.update(text_ger)
    letter_storage.update(text_unk)

    eng_encoded = lab_3.main.encode_corpus(letter_storage, text_eng)
    unk_encoded = lab_3.main.encode_corpus(letter_storage, text_unk)
    ger_encoded = lab_3.main.encode_corpus(letter_storage, text_ger)

    language_detector = lab_3.main.ProbabilityLanguageDetector((3, 4, 5), 1000)
    language_detector.new_language(eng_encoded, 'english')
    language_detector.new_language(ger_encoded, 'german')

    ngram_unknown = lab_3.main.NGramTrie(4)
    ngram_unknown.fill_n_grams(unk_encoded)

    actual = language_detector.detect_language(ngram_unknown.n_grams)

    RESULT = actual['german'] > actual['english']
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == 1
