"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':
    unknown_text = open('lab_3/unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')
    text_in_german = open('lab_3/Thomas_Mann.txt', encoding='utf-8')
    text_in_english = open('lab_3/Frank_Baum.txt', encoding='utf-8')

    unknown_tuple_text = lab_3.main.tokenize_by_sentence(unknown_text.read())
    german_tuple_text = lab_3.main.tokenize_by_sentence(text_in_german.read())
    english_tuple_text = lab_3.main.tokenize_by_sentence(text_in_english.read())

    unknown_text.close()
    text_in_german.close()
    text_in_english.close()

    # here goes your function calls
    letter_storage = lab_3.main.LetterStorage()
    letter_storage.update(english_tuple_text)
    letter_storage.update(german_tuple_text)
    letter_storage.update(unknown_tuple_text)

    unknown_encoded_text = lab_3.main.encode_corpus(letter_storage, unknown_tuple_text)
    english_encoded_text = lab_3.main.encode_corpus(letter_storage, english_tuple_text)
    german_encoded_text = lab_3.main.encode_corpus(letter_storage, german_tuple_text)

    language_detector = lab_3.main.ProbabilityLanguageDetector((3, 4, 5), 1000)
    language_detector.new_language(english_encoded_text, 'English')
    language_detector.new_language(german_encoded_text, 'German')

    ngram_trie_unknown = lab_3.main.NGramTrie(4)
    ngram_trie_unknown.fill_n_grams(unknown_encoded_text)

    RESULT = language_detector.detect_language(ngram_trie_unknown.n_grams)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT['English'] < RESULT['German'], 'Language detector does not work.'
