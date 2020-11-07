def clean_tokenize_corpus(texts: list) -> list:
    pass

    if not texts:
        return []

    tokenized_text_list = []

    for text in texts:

        # skipping non-string items in passed texts
        if type(text) is not str:
            continue

        # removing line breaks
        text = text.replace('<br />', ' ')

        # leaving only lowercase letters and spaces
        stripped_text = ''
        for symbol in text:
            if symbol.isalpha() or symbol == ' ':
                stripped_text += symbol.lower()

        # splitting the words and adding tokenized text to the list
        tokenized_text_list.append(stripped_text.split())

    return tokenized_text_list


class TfIdfCalculator:
    def __init__(self, corpus):
        pass
        self.corpus = []

        # clean up all the garbage from the passed corpus at object construction (retain only string words)
        if corpus:
            for text in corpus:
                if not text:
                    continue
                clean_text = []
                for word in text:
                    if type(word) is str:
                        clean_text.append(word)
                self.corpus.append(clean_text)

        self.tf_values = []
        self.idf_values = {}
        self.tf_idf_values = []

    def calculate_tf(self):
        pass

        for text in self.corpus:

            tf_text = {}
            len_text = len(text)

            for word in text:
                if word in tf_text:
                    # incrementing tf if already in the dictionary
                    tf_text[word] += 1 / len_text
                else:
                    # setting initial tf value if not
                    tf_text[word] = 1 / len_text

            # adding dictionary with tf values for the text to the list
            self.tf_values.append(tf_text)
        return

    def calculate_idf(self):
        pass

        texts_count = len(self.corpus)

        for index in range(texts_count):
            for word in self.corpus[index]:

                # skipping if idf has been already calculated for that word
                if word not in self.idf_values:

                    # we already got at least one entry
                    word_in_texts = 1

                    # and checking if we have more entries in subsequent texts
                    next_text_index = index + 1
                    while next_text_index < texts_count:
                        if word in self.corpus[next_text_index]:
                            word_in_texts += 1
                        next_text_index += 1

                    self.idf_values[word] = math.log(texts_count / word_in_texts)

        return

    def calculate(self):
        pass

        if not self.tf_values or not self.idf_values:
            return

        for tf_dict in self.tf_values:
            tf_idf_dict = {}
            for key, value in tf_dict.items():
                tf_idf_dict[key] = value * self.idf_values[key]
            self.tf_idf_values.append(tf_idf_dict)

        return

    def report_on(self, word, document_index):
        pass

        if not self.tf_idf_values or document_index >= len(self.tf_idf_values):
            return ()

        # converting tf_idf values for the provided document to a list sorted by tf_idf value, descending
        tf_idf_values_list = []
        for key, value in self.tf_idf_values[document_index].items():
            tf_idf_values_list.append((key, value))

        tf_idf_values_list.sort(key=lambda x: x[1], reverse=True)

        # looking up for the provided word and returning it's position in the sorted list (rating) if found
        index = 0
        while index < len(tf_idf_values_list):
            if tf_idf_values_list[index][0] == word:
                return (tf_idf_values_list[index][1], index)
            index += 1

        return ()
