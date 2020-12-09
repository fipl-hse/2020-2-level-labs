"""
Example of running generator
"""


from lab_4.main import tokenize_by_sentence, WordStorage, encode_text, NGramTextGenerator
from lab_4.ngrams.ngram_trie import NGramTrie


if __name__ == "__main__":
    TEXT = """
    The city where I live.
    My name is Clark, and I will tell you about my city.
    I live in an apartment. 
    In my city, there is a post office where people mail letters. 
    On Monday, I go to work. 
    I work at the post office. 
    Everyone shops for food at the grocery store. 
    They also eat at the restaurant. 
    The restaurant serves pizza and ice cream.
    My friends and I go to the park. 
    We like to play soccer at the park. 
    On Fridays, we go to the cinema to see a movie. 
    Children don't go to school on the weekend. 
    Each day, people go to the hospital when they are sick. 
    The doctors and nurses take care of them in the city. 
    The police keep everyone safe. I am happy to live in my city.
    """

    corpus = tokenize_by_sentence(TEXT)

    word_storage = WordStorage()
    word_storage.update(corpus)

    encoded_corpus = encode_text(word_storage, corpus)

    ngrams = NGramTrie(3, encoded_corpus)

    generator = NGramTextGenerator(word_storage, ngrams)

    context = (word_storage.get_id('the'),
               word_storage.get_id('post'))

    RESULT = generator.generate_text(context, 1)
    print(' '.join([word_storage.get_word(word) for word in RESULT]))
    assert RESULT, 'Language generator work incorrect'
