"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls

    eng_file = open('Frank_Baum.txt', encoding='utf-8')
    germ_file = open('Thomas_Mann.txt', encoding='utf-8')
    unk_file = open('unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')

    eng_text = lab_3.main.tokenize_by_sentence(eng_file.read())
    germ_text = lab_3.main.tokenize_by_sentence(germ_file.read())
    unk_text = lab_3.main.tokenize_by_sentence(unk_file.read())

    eng_file.close()
    germ_file.close()
    unk_file.close()

    letter_storage = lab_3.main.LetterStorage()
    letter_storage.update(eng_text)
    letter_storage.update(germ_text)
    letter_storage.update(unk_text)

    encoded_eng = lab_3.main.encode_corpus(letter_storage, eng_text)
    encoded_germ = lab_3.main.encode_corpus(letter_storage, germ_text)
    encoded_unk = lab_3.main.encode_corpus(letter_storage, unk_text)

    language_detector = lab_3.main.LanguageDetector((3, 4, 5), 1000)
    language_detector.new_language(encoded_eng, 'english')
    language_detector.new_language(encoded_germ, 'german')

    ngram_unknown = lab_3.main.NGramTrie(3)
    ngram_unknown.fill_n_grams(encoded_unk)

    actual = language_detector.detect_language(ngram_unknown.n_grams)

    RESULT = actual['german'] > actual['english']
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == 1, "Detector does not work"
