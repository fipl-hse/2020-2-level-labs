"""
Language detector implementation starter
"""

from lab_3.main import tokenize_by_sentence, LetterStorage, encode_corpus, ProbabilityLanguageDetector, NGramTrie

if __name__ == '__main__':

    print('Reading text files and tokenizing.\n')
    with open('lab_3/Frank_Baum.txt', encoding='utf-8') as english_file:
        english_text = tokenize_by_sentence(english_file.read())

    with open('lab_3/Thomas_Mann.txt', encoding='utf-8') as german_file:
        german_text = tokenize_by_sentence(german_file.read())

    with open('lab_3/unknown_Vorleser.txt', encoding='utf-8') as unknown_file:
        unknown_text = tokenize_by_sentence(unknown_file.read())

    print(f'''English text: {english_text[0]}
German text: {german_text[0]}
Unknown text: {unknown_text[0]}

''')

    print('Creating a letter storage and filling it with letters from texts.')
    letter_storage = LetterStorage()
    letter_storage.update(english_text)
    letter_storage.update(german_text)
    letter_storage.update(unknown_text)

    print(letter_storage.storage, '\n')

    print('Processing texts encoding')
    english_encoded = encode_corpus(letter_storage, english_text)
    german_encoded = encode_corpus(letter_storage, german_text)
    unknown_encoded = encode_corpus(letter_storage, unknown_text)

    print('English example: ', english_encoded[0], '\n')

    print('Creating language detector with different n-gram tries and top_k-s')

    for level in (2, 5, 10):
        ngram_unknown = NGramTrie(level)
        ngram_unknown.fill_n_grams(unknown_encoded)
        for top_k in (600, 1000, 2500):
            language_detector = ProbabilityLanguageDetector((level,), top_k)
            language_detector.new_language(english_encoded, 'english')
            language_detector.new_language(german_encoded, 'german')

            actual = language_detector.detect_language(ngram_unknown.n_grams)

            print('top_k =', top_k, 'level =', level, actual)
            if top_k == 600 and level == 5:
                RESULT = actual

    print('\nSo, when level = 2, detector works maximally correctly;\nby level = 5 and 10 it works incorrectly.'
          '\nTop_k doesn\'t change the result')

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT['english'] > RESULT['german'], 'The detector doesn\'t work.'
