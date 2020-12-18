# pylint: skip-file
"""
Tests for LanguageDetector class
"""

import unittest
from lab_3.main import tokenize_by_sentence
from lab_3.main import encode_corpus
from lab_3.main import NGramTrie
from lab_3.main import LetterStorage
from lab_3.main import LanguageDetector
from unittest.mock import patch

class LanguageDetectorTest(unittest.TestCase):
    """
    Checks for LanguageDetector class
    """
 
    def test_language_detector_creates_correctly(self):
        language_detector = LanguageDetector((3,), 10)
        self.assertEqual(language_detector.trie_levels, (3,))
        self.assertEqual(language_detector.top_k, 10)
        self.assertEqual(language_detector.n_gram_storages, {})

# ---------------------------------------------------------------
  
    def test_new_language_ideal_case(self):
        letter_storage = LetterStorage()
        language_detector = LanguageDetector((3,), 10)

        file = open('lab_3/Frank_Baum.txt', 'r', encoding='utf-8')
        text = tokenize_by_sentence(file.read())
        letter_storage.update(text)
        encoded_text = encode_corpus(letter_storage, text)
        file.close()

        language_detector.new_language(encoded_text, 'english')
        self.assertTrue(language_detector.n_gram_storages['english'])
        self.assertEqual(type(language_detector.n_gram_storages['english'][3]), NGramTrie)
 
    def test_new_language_incorrect_input(self):
        language_detector = LanguageDetector((3,), 10)

        expected = 1
        bad_inputs = [[], {}, '', 123, None, True, (None,)]
        for bad_input in bad_inputs:
            actual = language_detector.new_language(bad_input, 'english')
            self.assertEqual(expected, actual)

    def test_new_language_incorrect_language_input(self):
        language_detector = LanguageDetector((3,), 10)

        expected = 1
        patches_encoded_text = (((),),)
        bad_inputs = [[], {}, (), 123, None, True]
        for bad_input in bad_inputs:
            actual = language_detector.new_language(patches_encoded_text, bad_input)
            self.assertEqual(expected, actual)
    
    def test_new_language_storage_already_created(self):
        letter_storage = LetterStorage()
        language_detector = LanguageDetector((3,), 10)

        file = open('lab_3/Thomas_Mann.txt', 'r', encoding='utf-8')
        file_unknown = open('lab_3/unknown_Arthur_Conan_Doyle.txt', 'r', encoding='utf-8')
        text = tokenize_by_sentence(file.read())
        text_unknown = tokenize_by_sentence(file_unknown.read())
        letter_storage.update(text)
        letter_storage.update(text_unknown)
        encoded_text = encode_corpus(letter_storage, text)
        encoded_unknown_text = encode_corpus(letter_storage, text_unknown)
        file.close()
        file_unknown.close()

        language_detector.new_language(encoded_text, 'german')
        language_detector.new_language(encoded_unknown_text, 'english')
        self.assertTrue(language_detector.n_gram_storages['german'])
        self.assertTrue(language_detector.n_gram_storages['english'])
        self.assertEqual(type(language_detector.n_gram_storages['german'][3]), NGramTrie)
        self.assertEqual(type(language_detector.n_gram_storages['english'][3]), NGramTrie)
   
    def test_new_language_add_existing_language(self):
        letter_storage = LetterStorage()
        language_detector = LanguageDetector((3,), 10)

        file = open('lab_3/Frank_Baum.txt', 'r', encoding='utf-8')
        text = tokenize_by_sentence(file.read())
        letter_storage.update(text)
        encoded_text = encode_corpus(letter_storage, text)
        file.close()

        expected = 0
        language_detector.new_language(encoded_text, 'german')
        actual = language_detector.new_language(encoded_text, 'german')
        self.assertEqual(expected, actual)
    
    def test_new_language_creates_several_ngrams(self):
        letter_storage = LetterStorage()
        language_detector = LanguageDetector((2, 3), 10)

        file = open('lab_3/Frank_Baum.txt', 'r', encoding='utf-8')
        text = tokenize_by_sentence(file.read())
        letter_storage.update(text)
        encoded_text = encode_corpus(letter_storage, text)
        file.close()

        language_detector.new_language(encoded_text, 'english')
        self.assertTrue(language_detector.n_gram_storages['english'][2])
        self.assertTrue(language_detector.n_gram_storages['english'][3])

# ----------------------------------------------------------------------------
   
    def test_calculate_distance_ideal(self):
        language_detector = LanguageDetector((2, 3), 10)

        first_n_grams = ((1, 2), (3, 4), (7, 8), (9, 10), (5, 6), (13, 14))
        second_n_grams = ((1, 2), (5, 6), (7, 8), (3, 4), (11, 12), (15, 16))

        expected = 17
        actual = language_detector._calculate_distance(first_n_grams, second_n_grams)
        self.assertEqual(expected, actual)
 
    def test_calculate_distance_incorrect_input(self):
        language_detector = LanguageDetector((3, ), 10)

        patches_ngrams = ((1, 2), (3, 4), (7, 8), (9, 10), (5, 6), (13, 14))

        expected = -1
        bad_inputs = [[], {}, '', 1, -1, 9.22, None, True, (None,)]
        for bad_input in bad_inputs:
            actual_first = language_detector._calculate_distance(bad_input,
                                                                 patches_ngrams)
            actual_second = language_detector._calculate_distance(patches_ngrams,
                                                                  bad_input)
            self.assertEqual(expected, actual_first)
            self.assertEqual(expected, actual_second)

    def test_calculate_distance_is_empty(self):
        language_detector = LanguageDetector((3,), 10)

        empty_sentence = ()
        patches_sentence = ('th', 'er', 'on', 'le', 'ing', 'and')
        expected = 0
        actual_first = language_detector._calculate_distance(empty_sentence,
                                                             patches_sentence)
        actual_second = language_detector._calculate_distance(patches_sentence,
                                                              empty_sentence)
        self.assertEqual(expected, actual_first)
        self.assertEqual(expected, actual_second)

# ------------------------------------------------------------------------------
   
    def test_detect_language_ideal(self):
        letter_storage = LetterStorage()
        language_detector = LanguageDetector((3,), 100)

        file_first = open('lab_3/Frank_Baum.txt', 'r', encoding='utf-8')
        file_second = open('lab_3/Thomas_Mann.txt', 'r', encoding='utf-8')
        file_third = open('lab_3/unknown_Arthur_Conan_Doyle.txt', 'r', encoding='utf-8')

        text_english = tokenize_by_sentence(file_first.read())
        text_german = tokenize_by_sentence(file_second.read())
        text_unknown = tokenize_by_sentence(file_third.read())
        letter_storage.update(text_english)
        letter_storage.update(text_german)
        letter_storage.update(text_unknown)
        encoded_english = encode_corpus(letter_storage, text_english)
        encoded_german = encode_corpus(letter_storage, text_german)
        encoded_unknown = encode_corpus(letter_storage, text_unknown)
        file_first.close()
        file_second.close()
        file_third.close()

        language_detector.new_language(encoded_english, 'english')
        language_detector.new_language(encoded_german, 'german')

        actual = language_detector.detect_language(encoded_unknown)
        self.assertTrue(actual['english'] > actual['german'])

 
    def test_detect_language_incorrect_text_input(self):
        language_detector = LanguageDetector((3,), 10)

        expected = {}
        bad_inputs = [[], {}, set(), '', 123, -1, 0.7, None, True, (None,)]
        for bad_input in bad_inputs:
            actual = language_detector.detect_language(bad_input)
            self.assertEqual(expected, actual)
    
    def test_detect_language_empty_text_input(self):
        language_detector = LanguageDetector((3,), 10)

        encoded_text = ()
        expected = {}
        actual = language_detector.detect_language(encoded_text)
        self.assertEqual(expected, actual)
    
    @patch('lab_3.main.LanguageDetector._calculate_distance', side_effect=LanguageDetector()._calculate_distance)

    def test_detect_language_calls_required_method(self, mock):
        letter_storage = LetterStorage()
        language_detector = LanguageDetector((3,), 10)
        text_to_detect = (((1, 2, 3),),)
        file = open('lab_3/Frank_Baum.txt', 'r', encoding='utf-8')
        text = tokenize_by_sentence(file.read())
        letter_storage.update(text)
        encoded_text = encode_corpus(letter_storage, text)
        file.close()
        language_detector.new_language(encoded_text, 'english')
        language_detector.detect_language(text_to_detect)
        self.assertTrue(mock.called)

    def test_detect_language_uses_several_ngrams(self):
        letter_storage = LetterStorage()
        language_detector = LanguageDetector((2, 3), 100)

        file_first = open('lab_3/Frank_Baum.txt', 'r', encoding='utf-8')
        file_second = open('lab_3/Thomas_Mann.txt', 'r', encoding='utf-8')
        file_third = open('lab_3/unknown_Arthur_Conan_Doyle.txt', 'r', encoding='utf-8')

        text_english = tokenize_by_sentence(file_first.read())
        text_german = tokenize_by_sentence(file_second.read())
        text_unknown = tokenize_by_sentence(file_third.read())
        letter_storage.update(text_english)
        letter_storage.update(text_german)
        letter_storage.update(text_unknown)
        encoded_english = encode_corpus(letter_storage, text_english)
        encoded_german = encode_corpus(letter_storage, text_german)
        encoded_unknown = encode_corpus(letter_storage, text_unknown)
        file_first.close()
        file_second.close()
        file_third.close()

        language_detector.new_language(encoded_english, 'english')
        language_detector.new_language(encoded_german, 'german')

        actual = language_detector.detect_language(encoded_unknown)
        self.assertTrue(actual['german'] > actual['english'])
  
    def test_detect_language_not_filled_ngram_storages(self):
        language_detector = LanguageDetector((2, 3), 100)

        patches_sentence = (((1, 2, 3),),)

        expected = {}
        actual = language_detector.detect_language(patches_sentence)
        self.assertEqual(expected, actual)
