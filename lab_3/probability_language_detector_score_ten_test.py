# pylint: skip-file
"""
Tests for ProbabilityLanguageDetector class
"""


import unittest
from lab_3.main import NGramTrie
from lab_3.main import tokenize_by_sentence
from lab_3.main import encode_corpus
from lab_3.main import LetterStorage
from lab_3.main import ProbabilityLanguageDetector
from unittest.mock import patch


class ProbabilityLanguageDetectorTest(unittest.TestCase):
    """
    Checks for ProbabilityLanguageDetector class
    """

    @unittest.skip('')
    def test_probability_language_detector_check_creation(self):
        language_detector = ProbabilityLanguageDetector((3, 5), 10)
        self.assertEqual(language_detector.trie_levels, (3, 5))
        self.assertEqual(language_detector.top_k, 10)
        self.assertEqual(language_detector.n_gram_storages, {})

    @unittest.skip('')
    def test_probability_language_detector_calculate_probability_ideal(self):
        english_file = open('lab_3/Frank_Baum.txt', encoding='utf-8')
        german_file = open('lab_3/Thomas_Mann.txt', encoding='utf-8')
        unknown_file = open('lab_3/unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')

        english_text = tokenize_by_sentence(english_file.read())
        german_text = tokenize_by_sentence(german_file.read())
        unknown_text = tokenize_by_sentence(unknown_file.read())

        english_file.close()
        german_file.close()
        unknown_file.close()

        letter_storage = LetterStorage()
        letter_storage.update(english_text)
        letter_storage.update(german_text)
        letter_storage.update(unknown_text)

        english_encoded = encode_corpus(letter_storage, english_text)
        german_encoded = encode_corpus(letter_storage, german_text)
        unknown_encoded = encode_corpus(letter_storage, unknown_text)

        language_detector = ProbabilityLanguageDetector((3,), 1000)
        language_detector.new_language(english_encoded, 'english')
        language_detector.new_language(german_encoded, 'german')

        n3_gram_trie_english = language_detector.n_gram_storages['english'][3]
        n3_gram_trie_german = language_detector.n_gram_storages['german'][3]

        n3_gram_unknown = NGramTrie(3)
        n3_gram_unknown.fill_n_grams(unknown_encoded)

        english_prob = language_detector._calculate_sentence_probability(n3_gram_trie_english,
                                                                         n3_gram_unknown.n_grams)
        german_prob = language_detector._calculate_sentence_probability(n3_gram_trie_german,
                                                                        n3_gram_unknown.n_grams)
        print(f'English_sentence_prob: {english_prob}')
        print(f'Deutsch_sentence_prob: {german_prob}')
        self.assertTrue(english_prob > german_prob)

    @unittest.skip('')
    def test_probability_language_detector_calculate_probability_incorrect_storage(self):
        language_detector = ProbabilityLanguageDetector((2, 3), 10)
        bad_inputs = [(), [], {}, '', None, True, set()]
        patches_encoded_unknown = (((),),)

        expected = -1.0
        for bad_input in bad_inputs:
            actual = language_detector._calculate_sentence_probability(bad_input,
                                                                       patches_encoded_unknown)
            self.assertEqual(expected, actual)

    @unittest.skip('')
    def test_probability_language_detector_calculate_probability_incorrect_text(self):
        language_detector = ProbabilityLanguageDetector((2, 3), 10)
        bad_inputs = [[], {}, '', None, True, set()]
        ngram_trie = NGramTrie(5)

        expected = -1.0
        for bad_input in bad_inputs:
            actual = language_detector._calculate_sentence_probability(ngram_trie,
                                                                       bad_input)
            self.assertEqual(expected, actual)

    @unittest.skip('')
    def test_probability_language_detector_several_ngrams_case(self):
        language_detector = ProbabilityLanguageDetector((3, 5), 1000)

        english_file = open('lab_3/Frank_Baum.txt', encoding='utf-8')
        german_file = open('lab_3/Thomas_Mann.txt', encoding='utf-8')
        unknown_file = open('lab_3/unknown_Arthur_Conan_Doyle.txt', encoding='utf-8')

        eng_text = tokenize_by_sentence(english_file.read())
        ger_text = tokenize_by_sentence(german_file.read())
        unk_text = tokenize_by_sentence(unknown_file.read())

        english_file.close()
        german_file.close()
        unknown_file.close()

        letter_storage = LetterStorage()
        letter_storage.update(eng_text)
        letter_storage.update(ger_text)
        letter_storage.update(unk_text)

        english_encoded = encode_corpus(letter_storage, eng_text)
        german_encoded = encode_corpus(letter_storage, ger_text)
        unknown_encoded = encode_corpus(letter_storage, unk_text)

        language_detector.new_language(english_encoded, 'english')
        language_detector.new_language(german_encoded, 'german')

        eng_prob = language_detector.n_gram_storages['english'][5]
        ger_prob = language_detector.n_gram_storages['german'][5]

        ngram_trie = NGramTrie(5)
        ngram_trie.fill_n_grams(unknown_encoded)

        eng = language_detector._calculate_sentence_probability(eng_prob, ngram_trie.n_grams)
        ger = language_detector._calculate_sentence_probability(ger_prob, ngram_trie.n_grams)
        self.assertTrue(ger > eng)

    @unittest.skip('')
    def test_probability_language_detector_detect_language_ideal(self):
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

        language_detector = ProbabilityLanguageDetector((3, 4, 5), 1000)
        language_detector.new_language(eng_encoded, 'english')
        language_detector.new_language(ger_encoded, 'german')

        ngram_unknown = NGramTrie(4)
        ngram_unknown.fill_n_grams(unk_encoded)

        actual = language_detector.detect_language(ngram_unknown.n_grams)
        self.assertTrue(actual['german'] > actual['english'])

    @unittest.skip('')
    def test_probability_language_detector_detect_incorrect(self):
        language_detector = ProbabilityLanguageDetector((3, 5), 100)
        bad_inputs = [[], {}, '', 1, None, True, (None,)]

        expected = {}
        for bad_input in bad_inputs:
            actual = language_detector.detect_language(bad_input)
            self.assertEqual(expected, actual)

    @patch('lab_3.main.ProbabilityLanguageDetector._calculate_sentence_probability',
           side_effect=ProbabilityLanguageDetector()._calculate_sentence_probability)
    @unittest.skip('')
    def test_probability_language_detector_calls_required_method(self, mock):
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

        language_detector = ProbabilityLanguageDetector((3, 4, 5), 1000)
        language_detector.new_language(eng_encoded, 'english')
        language_detector.new_language(ger_encoded, 'german')

        ngram_unknown = NGramTrie(4)
        ngram_unknown.fill_n_grams(unk_encoded)

        language_detector.detect_language(ngram_unknown.n_grams)
        self.assertTrue(mock.called)
