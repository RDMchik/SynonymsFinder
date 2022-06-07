from io import StringIO
from typing import Optional

import re


# creating a class which is going to read from file
class FileReader(object):
    _directory = None

    def __init__(self, directory: str, filter: Optional[bool] = False) -> None:
        self._directory = directory
        self.data = self.load()

        if filter: # replacing \n from the text with space
            self.data = self.data.replace('\n', '')    

    def load(self):
        with open(self._directory, 'r', encoding='utf-8') as file:
            data = file.read()
        return str(data)

    def __str__(self):
        return self.data


# creating string builder class 
class StringBuilder(object): 
    _file_str = None

    def __init__(self, to_add: Optional[str] = None) -> None:
        self._file_str = StringIO()

        if to_add:
            self.add(to_add)

    def add(self, string_value: str):
        self._file_str.write(string_value)

    def __str__(self):
        return self._file_str.getvalue()


# creating a manager where the main logic will stay at
class Manager(object):
    _sentences = None

    def __init__(self, text: FileReader, synonyms: list, word: str) -> None:
        self.text = StringBuilder(str(text))
        self.synonyms = synonyms
        self.word = word.lower()

        self._sentences = self._get_sentences()

    def get_synonyms_chances(self): # looking and checking synonyms chance
        total_word_found = 0
        word_sentences = [] # sentences with the main word inside

        chances = {}

        for sentence in self._sentences:
            if self.word in sentence.lower():
                total_word_found += 1 # add plus one if found the main word (used for chance calculation)
                word_sentences.append(sentence) 

        for synonym in self.synonyms:
            for sentence in self._sentences:
                sentence = sentence.lower()
                if not str(synonym).lower() in sentence: # continue if synonym not in the sentence
                    continue
                print(synonym, 'in here!', sentence)
                similarity_procents = []
                for word_sentence in word_sentences:
                    total_words_similarity = 0
                    for word in re.split(' ', sentence):
                        if word in word_sentence:
                            total_words_similarity += 1
                    num = float(total_words_similarity / len(re.split(' ', word_sentence)))
                    similarity_procents.append(num)
                final_procent = 0.0
                for num in similarity_procents:
                    final_procent += num
                final_procent /= len(similarity_procents)
                chances[str(synonym)] = str(int(final_procent * 100)) + '%'

        return chances

    def _get_sentences(self):
        return re.split('\. |\! |\? ', str(self.text))


# starting from here ^^

text = FileReader('text.txt', True)

word = str(input('please enter a word: '))
synonyms = str(input('now write synonyms to check for (user space to add a few): '))

synonyms = re.split(' ', synonyms)

manager = Manager(text, synonyms, word)

print(manager.get_synonyms_chances())

# i recheked it a few times, looks like it works the right way. In order to get a more accurate
# result, you could just expand the text.txt file more (there is a text about politics and dogs)
# if the program returns {} or an error, that means no synonyms was found.