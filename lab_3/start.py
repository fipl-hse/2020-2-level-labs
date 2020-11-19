"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':
    # here goes your function calls
    letter_storage = lab_3.main.LetterStorage()
    language_detector = lab_3.main.LanguageDetector((3, 5), 150)

    file_first = open("lab_3/Frank_Baum.txt", 'r', encoding='utf-8')
    file_second = open("lab_3/Thomas_Mann.txt", 'r', encoding='utf-8')
    TEXT = """
    Extroversion is conducive to working well with people. 
    One of the things that characterizes extroverts is they need stimulation. 
    And that stimulation can be achieved by finding things that are exciting: loud noises, parties and social events. 
    The extroverts form a magnetic core. 
    They all gather together. 
    The introverts are more likely to spend time in the quiet spaces, where they are able to reduce stimulation. 
    They are not necessarily antisocial. 
    It may be that you simply realize that you do better when you have a chance to lower that level of stimulation.
    We communicate differently, extroverts and introverts. 
    Extroverts, when they interact, want to have lots of social encounter punctuated by closeness. 
    They'd like to stand close for comfortable communication. 
    They like to have a lot of eye contact, or mutual gaze. 
    Extroverts prefer black-and-white, concrete, simple language. 
    Introverts prefer contextually complex, contingent, weasel-word sentences.
    """

    text_english = lab_3.main.tokenize_by_sentence(file_first.read())
    text_german = lab_3.main.tokenize_by_sentence(file_second.read())
    text_unknown = lab_3.main.tokenize_by_sentence(TEXT)
    letter_storage.update(text_english)
    letter_storage.update(text_german)
    letter_storage.update(text_unknown)
    encoded_english = lab_3.main.encode_corpus(letter_storage, text_english)
    encoded_german = lab_3.main.encode_corpus(letter_storage, text_german)
    encoded_unknown = lab_3.main.encode_corpus(letter_storage, text_unknown)
    file_first.close()
    file_second.close()

    language_detector.new_language(encoded_english, 'english')
    language_detector.new_language(encoded_german, 'german')

    RESULT = language_detector.detect_language(encoded_unknown)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    print(RESULT)
    assert RESULT['german'] > RESULT['english'], 'Not working'
