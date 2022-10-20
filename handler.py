from enum import Enum
from Spellchecker import Spellchecker
from abc import ABC, abstractmethod
from nltk.tokenize import word_tokenize
import re


class HandlerModes(Enum):
    Autocorrect = 0,
    Highlight = 1


class HandlerABC(ABC):
    words = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self):
        with open("en-base.txt", 'r') as base:
            self.words = set(re.findall(r'\w+', base.read().lower()))

        self.spellchecker = Spellchecker(self.words, self.alphabet)
        self.previous_separator_index = (1, -1)
        self.last_separator_index = self.previous_separator_index
        self.text = ''

    @abstractmethod
    def handle(self, text: str) -> (dict, bool):
        pass

    def get_format_indexes(self, word: str) -> (str, str):
        index_in_line = self.text.find(word)
        row_index = self.text[:index_in_line].count('\n') + 1
        column_index_start = len(self.text[self.text[:-1].rfind('\n') + 1: index_in_line])
        column_index_end = column_index_start + len(word)

        return f'{row_index}.{column_index_start}', f'{row_index}.{column_index_end}'


class AutoCorrect_Handler(HandlerABC):

    def __init__(self):
        super().__init__()

    def handle(self, text: str) -> (dict, bool):
        self.text = text
        all_tokens = word_tokenize(text)

        if len(all_tokens) < 2:
            return {}, False

        word = all_tokens[-2]
        corrected = self.spellchecker._correct(word)

        return ({corrected: self.get_format_indexes(word)}, True) \
            if word != corrected \
            else ({word: self.get_format_indexes(word)}, False)


class Highlight_Handler(HandlerABC):

    def __init__(self):
        super().__init__()

    def handle(self, text: str) -> (dict, bool):
        self.text = text
        all_tokens = word_tokenize(text)
        all_tokens = all_tokens[:len(all_tokens) - 1]
        word_tokens = [literal for literal in all_tokens if literal.isalpha()]

        bindings = {}
        for token in word_tokens:
            if token != self.spellchecker._correct(token):
                bindings[token] = self.get_format_indexes(token)

        return bindings, True


class Handler:
    @staticmethod
    def create(mode: HandlerModes) -> HandlerABC:
        if mode == HandlerModes.Highlight:
            return Highlight_Handler()
        if mode == HandlerModes.Autocorrect:
            return AutoCorrect_Handler()
