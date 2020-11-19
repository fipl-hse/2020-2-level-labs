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
    english_file = open('lab_3/Frank_Baum.txt', encoding='utf-8')

    unknown_text = tokenize_by_sentence(unknown_file.read())
    german_text = tokenize_by_sentence(german_file.read())
    english_text = tokenize_by_sentence(english_file.read())
    english_file.close()
    german_file.close()
    unknown_file.close()

    letter_storage = LetterStorage()
    letter_storage.update(english_text)
    letter_storage.update(german_text)
    letter_storage.update(unknown_text)

    eng_encoded = encode_corpus(letter_storage, english_text)
    unk_encoded = encode_corpus(letter_storage, unknown_text)
    ger_encoded = encode_corpus(letter_storage, german_text)

    language_detector = LanguageDetector((3, 4, 5), 1000)
    language_detector.new_language(eng_encoded, 'english')
    language_detector.new_language(ger_encoded, 'german')

    ngram_unknown = NGramTrie(4)
    ngram_unknown.fill_n_grams(unk_encoded)

    language_log_probability_dict = language_detector.detect_language(ngram_unknown.n_grams)

    if language_log_probability_dict['german'] > language_log_probability_dict['english']:
        RESULT = 'english'
    else:
        RESULT = 'german'

    print('It is a {} text.'.format(RESULT))

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == 'english', 'Not working'
