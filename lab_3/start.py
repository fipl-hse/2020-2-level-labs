"""
Language detector implementation starter
"""

from lab_3.main import tokenize_by_sentence, NGramTrie
from lab_3.main import LetterStorage
from lab_3.main import encode_corpus
from lab_3.main import ProbabilityLanguageDetector

if __name__ == '__main__':
    english_language = open('lab_3/Frank_Baum.txt', encoding='utf-8')
    german_language = open('lab_3/Thomas_Mann.txt', encoding='utf-8')
    unknown_language = open('lab_3/unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')

    eng_text = tokenize_by_sentence(english_language.read())
    germ_text = tokenize_by_sentence(german_language.read())
    unkn_text = tokenize_by_sentence(unknown_language.read())

    english_language.close()
    german_language.close()
    unknown_language.close()

    letter_storage = LetterStorage()
    letter_storage.update(eng_text)
    letter_storage.update(germ_text)
    letter_storage.update(unkn_text)

    encoded_eng = encode_corpus(letter_storage, eng_text)
    encoded_germ = encode_corpus(letter_storage, germ_text)
    encoded_unkn = encode_corpus(letter_storage, unkn_text)

    language_detector = ProbabilityLanguageDetector((3, 4, 5), 1000)
    language_detector.new_language(encoded_eng, 'english')
    language_detector.new_language(encoded_germ, 'german')

    unknown_ngram = NGramTrie(4)
    unknown_ngram.fill_n_grams(encoded_unkn)

    # here goes your function calls
    actual = language_detector.detect_language(unknown_ngram.n_grams)

    RESULT = actual['german'] > actual['english']
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, "Doesn't work"
