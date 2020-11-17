"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls

    TEXT = '''Harry Potter was a highly unusual boy in many ways. For one thing, he hated the summer holidays more than
    any other time of year. For another, he really wanted to do his homework but was forced to do it in secret, in the
    dead of night. And he also happened to be a wizard.
    It was nearly midnight, and he was lying on his stomach in bed, the blankets drawn right over his head like a tent,
    a flashlight in one hand and a large leather-bound book (A History of Magic by Bathilda Bagshot) propped open
    against the pillow. Harry moved the tip of his eagle-feather quill down the page, frowning as he looked for
    something that would help him write his essay, 'Witch Burning in the Fourteenth Century Was Completely Pointless
    - discuss.'
    The quill paused at the top of a likely looking paragraph. Harry pushed his round glasses up the bridge of his nose,
    moved his flashlight closer to the book, and read:
    Non-magic people (more commonly known as Muggles) were particularly afraid of magic in medieval times, but not very
    good at recognizing it. On the rare occasion that they did catch a real witch or wizard, burning had no effect
    whatsoever. The witch or wizard would perform a basic Flame-Freezing Charm and then pretend to shriek with pain
    while enjoying a gentle, tickling sensation. Indeed, Wendelin the Weird enjoyed being burned so much that she
    allowed herself to be caught no less than forty-seven times in various disguises.
    Harry put his quill between his teeth and reached underneath his pillow for his inkbottle and a roll of parchment.
    Slowly and very carefully he unscrewed the ink bottle, dipped his quill into it, and began to write, pausing every
    now and then to listen, because if any of the Dursleys heard the scratching of his quill on their way to the
    bathroom, he'd probably find himself locked in the cupboard under the stairs for the rest of the summer.'''

    unknown_text = lab_3.main.tokenize_by_sentence(TEXT)

    english = open('lab_3/Frank_Baum.txt', encoding='utf-8')
    english_text = lab_3.main.tokenize_by_sentence(english.read())
    english.close()

    german = open('lab_3/Thomas_Mann.txt', encoding='utf-8')
    german_text = lab_3.main.tokenize_by_sentence(german.read())
    german.close()

    letter_storage = lab_3.main.LetterStorage()
    letter_storage.update(unknown_text)
    letter_storage.update(english_text)
    letter_storage.update(german_text)

    encoded_unknown_text = lab_3.main.encode_corpus(letter_storage, unknown_text)
    encoded_english_text = lab_3.main.encode_corpus(letter_storage, english_text)
    encoded_german_text = lab_3.main.encode_corpus(letter_storage, german_text)

    language_detector = lab_3.main.ProbabilityLanguageDetector((3, 4, 5), 500)
    language_detector.new_language(encoded_english_text, 'english')
    language_detector.new_language(encoded_german_text, 'german')

    n_gram_unknown = lab_3.main.NGramTrie(4)
    n_gram_unknown.fill_n_grams(encoded_unknown_text)

    language_log_probability_dict = language_detector.detect_language(n_gram_unknown.n_grams)

    if language_log_probability_dict['german'] > language_log_probability_dict['english']:
        RESULT = 'english'
    else:
        RESULT = 'german'

    print('The text is in {}'.format(RESULT))

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == 'english', 'Not working'
