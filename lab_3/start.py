"""
Language detector implementation starter
"""
from lab_3.main import tokenize_by_sentence
from lab_3.main import encode_corpus
from lab_3.main import NGramTrie
from lab_3.main import LetterStorage
from lab_3.main import ProbabilityLanguageDetector


if __name__ == '__main__':

    # here goes your function calls
    unknown_file = open('lab_3/unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')
    german_file = open('lab_3/Thomas_Mann.txt', encoding='utf-8')
    english_file = open('lab_3/Frank_Baum.txt', encoding='utf-8')

    text_unk = tokenize_by_sentence(unknown_file.read())
    text_ger = tokenize_by_sentence(german_file.read())
    text_eng = tokenize_by_sentence(english_file.read())
    english_file.close()
    german_file.close()
    unknown_file.close()

    letter_storage = LetterStorage()
    letter_storage.update(text_eng)
    letter_storage.update(text_ger)
    letter_storage.update(text_unk)

    eng_encoded = encode_corpus(letter_storage, text_eng)
    unk_encoded = encode_corpus(letter_storage, text_unk)
    ger_encoded = encode_corpus(letter_storage, text_ger)
    
    ngram_unknown = NGramTrie(2)
    ngram_unknown.fill_n_grams(unk_encoded)

    actual = language_detector.detect_language(ngram_unknown.n_grams)
    print(actual)

    RESULT = actual['english'] < actual['german']
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == 1, ''
