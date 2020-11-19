"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls
    english_file = open('Frank_Baum.txt', encoding='utf-8')
    german_file = open('Thomas_Mann.txt', encoding='utf-8')
    unknown_file = open('unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')

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

    english_encoded = lab_3.main.encode_corpus(letter_storage, english_text)
    german_encoded = lab_3.main.encode_corpus(letter_storage, german_text)
    unknown_encoded = lab_3.main.encode_corpus(letter_storage, unknown_text)

    language_detector = lab_3.main.ProbabilityLanguageDetector((3,), 1000)
    language_detector.new_language(english_encoded, 'english')
    language_detector.new_language(german_encoded, 'german')

    n3_gram_trie_english = language_detector.n_gram_storages['english'][3]
    n3_gram_trie_german = language_detector.n_gram_storages['german'][3]

    n3_gram_unknown = lab_3.main.NGramTrie(3)
    n3_gram_unknown.fill_n_grams(unknown_encoded)

    english_prob = language_detector._calculate_sentence_probability(n3_gram_trie_english,
                                                                     n3_gram_unknown.n_grams)
    german_prob = language_detector._calculate_sentence_probability(n3_gram_trie_german,
                                                                    n3_gram_unknown.n_grams)

    if english_prob > german_prob:
        RESULT = 'english'
    else:
        RESULT = 'german'

    print('{} language'.format(RESULT))
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == 'english', 'doesnt work'
