from Spelling import Spelling
import re


class Spellchecker:

    def __init__(self, words: set, alphabet: str):
        self.known_words = words
        self.alphabet = alphabet

    def check_word(self, word: str):
        if not word.isalpha():
            return None

        if word in self.known_words:
            return word
        else:
            return self.correct(word)

    def check_sentence(self, sentence: str, prettify=False):
        if sentence == '':
            return None
        result_sentence = sentence

        words = re.split(r'\W+', sentence)
        corrected = []
        for word in words:
            corrected_word = self.correct(word) if word.isalpha() else None
            if (corrected_word is None) or (corrected_word == word):
                continue

            result_sentence = result_sentence.replace(word, corrected_word)
            corrected.append(self._prettify_output(word, corrected_word) if prettify else corrected_word)

        return '\n'.join(corrected) if prettify else result_sentence

    def get_nearest(self, word: str):
        spelling = Spelling(word, self)
        return list(spelling.nearest_candidates())

    def correct(self, word: str, prettify=False):
        spelling = Spelling(word, self)
        correct = spelling.correct()

        return self._prettify_output(word, correct) if prettify else correct

    def _prettify_output(self, word_with_mistake, corrected_word) -> str:
        return f'{word_with_mistake} -> {corrected_word}'

    def correct_first_N(self, sentence: str, count: int) -> str:
        pass
