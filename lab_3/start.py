"""
Language detector implementation starter
"""

import main

if __name__ == '__main__':
    print('\t...opening files with texts...')
    unknown_file = open('lab_3/unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')
    german_file = open('lab_3/Thomas_Mann.txt', encoding='utf-8')
    english_file = open('lab_3/Frank_Baum.txt', encoding='utf-8')
    print('\t...tokenizing texts...')
    unknown_text = main.tokenize_by_sentence(unknown_file.read())
    german_text = main.tokenize_by_sentence(german_file.read())
    english_text = main.tokenize_by_sentence(english_file.read())
    english_file.close()
    german_file.close()
    unknown_file.close()
    print('\t...filling letter storages...')
    letter_storage = main.LetterStorage()
    letter_storage.update(english_text)
    letter_storage.update(german_text)
    letter_storage.update(unknown_text)
    print('\t...encoding sentences...')
    unknown_encoded = main.encode_corpus(letter_storage, unknown_text[:100])
    german_encoded = main.encode_corpus(letter_storage, german_text[:100])
    english_encoded = main.encode_corpus(letter_storage, english_text[:100])
    print('\t...creating n-grams...')
    language_detector = main.ProbabilityLanguageDetector((3, 4, 5), 100)
    language_detector.new_language(english_encoded, 'English')
    language_detector.new_language(german_encoded, 'German')
    n_gram_unknown = main.NGramTrie(4)
    n_gram_unknown.fill_n_grams(unknown_encoded)
    print('\t...detecting the language of the unknown file...')
    output = language_detector.detect_language(n_gram_unknown.n_grams)
    print('Probability:', output)
    RESULT = output
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, {'English': -4695.584268665556, 'German': -4052.9259031970378}
