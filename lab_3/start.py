"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls
    TEXT = '''Der Mond
    Der Mond ist das hellste und das groesste Objekt in unserem Nachthimmel. 
    Oft scheint es, dass er genauso wie die Sonne beim trueben Wetter scheint. 
    Aber in der Wirklichkeit hat der Mond keine Ausstrahlung. 
    Das ist eine riesengrosse kalte Steinkugel, die die Sonnenstrahlen widerspiegelt. 
    Der Mond ist der Satellit der Erde, welcher sich um unseren Planeten dreht.
    Die Mondoberflaeche ist mit vielen Kratern bedeckt. 
    Die Mondtrichter sind die Spuren der Zusammenstoesse mit verschiedenen Sternschuppen. 
    Sichtbare dunkle Flecken auf der Mondoberflaeche sind keine ehemaligen Meere, 
    wie die Menschen urspruenglich geglaubt haben. 
    Das sind grosse Flachfelder, die infolge von Vulkanausbruechen entstanden sind und aus Lava bestehen. 
    Auf dem Mond gibt es keine Atmosphaere und auf ihrer Oberflaeche existiert kein Leben. 
    Da die Luft hier fehlt, ist der Himmel ueber dem Mond immer schwarz und es gibt dort keinen Wind. 
    Vom Wort «Mond» ist das Wort «Monat» entstanden. 
    Ein Monat ist der Zeitraum, innerhalb von welchem der Mond sich ein Mal um die Erde dreht. 
    Von diesem Wort wurde das Wort «Monat» gebildet, das 1/12 des irdischen Jahres bedeutet.
    Der Mond ist das einzige Objekt im Weltraum, welches der Mensch besucht hat. 
    Der Amerikaner Nil Armstrong hat den Mond am 27. Juli 1969 betreten. 
    Danach sind viele Kosmonauten auf dem Mond gewesen. 
    Es ist sehr leicht, sich auf der Oberflaeche des Mondes zu bewegen, 
    weil die Schwerkraft auf unserem Satelliten sechs mal weniger als die irdische Schwerkraft ist. 
    Das heisst, alles wiegt hier auch sechs mal weniger.
    Ein Tag dauert auf dem Mond 360 Stunden. Genauso lange dauert eine Nacht auf dem Mond. 
    Die Tagestemperaturen koennen +130°С und die Nachttemperaturen -170°С erreichen.'''

    letter_storage = lab_3.main.LetterStorage()
    language_detector = lab_3.main.LanguageDetector((3, 4, 5), 100)

    file_first = open('lab_3/Frank_Baum.txt', 'r', encoding='utf-8')
    file_second = open('lab_3/Thomas_Mann.txt', 'r', encoding='utf-8')

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

    print('Detecting the language of the text by n-gram distances...')
    language_detector.new_language(encoded_english, 'english')
    language_detector.new_language(encoded_german, 'german')

    RESULT = language_detector.detect_language(encoded_unknown)
    print(RESULT)
    if RESULT['english'] > RESULT['german']:
        print('The text is probably german\n')
    else:
        print('The text is probably english\n')

    print('Detecting the language of the text by log probabilities...')
    language_detector_complex = lab_3.main.ProbabilityLanguageDetector((3, 4), 1000)
    language_detector_complex.new_language(encoded_english, 'english')
    language_detector_complex.new_language(encoded_german, 'german')

    ngram_unknown = lab_3.main.NGramTrie(3)
    ngram_unknown.fill_n_grams(encoded_unknown)

    actual = language_detector_complex.detect_language(ngram_unknown.n_grams)
    print(actual)
    if actual['german'] > actual['english']:
        print('I guess it`s german text')
    else:
        print('I guess it`s english text')

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT['english'] > RESULT['german'], 'Language was detected incorrectly'
