import unittest
from Spellchecker import Spellchecker
from Spelling import Spelling
import re


class SpellChecker_Tests(unittest.TestCase):

    def setUp(self) -> None:
        words = []
        with open("en-base.txt", 'r') as base:
            words = set(re.findall(r'\w+', base.read().lower()))

        alphabet = "abcdefghijklmnopqrstuvwxyz"

        self.spellchecker = Spellchecker(words, alphabet)

    def test_none_when_empty(self):
        self.assertIsNone(self.spellchecker.check_word(''))
        self.assertIsNone(self.spellchecker.check_sentence(''))

    def test_none_when_not_alpha(self):
        self.assertIsNone(self.spellchecker.check_word('123'))
        self.assertIsNone(self.spellchecker.check_word('mistakke3'))

    def test_itself_when_no_matching(self):
        self.assertEqual('asdfg', self.spellchecker.check_word('asdfg'))
        self.assertEqual('hylariooz', self.spellchecker.check_word('hylariooz'))
        self.assertEqual('nonmatching', self.spellchecker.check_word('nonmatching'))

    def test_simple_correct(self):
        self.assertEqual('mistake', self.spellchecker.check_word('mistacke'))
        self.assertEqual('ginger', self.spellchecker.check_word('ginjer'))
        self.assertEqual('simplify', self.spellchecker.check_word('simplifi'))
        self.assertEqual('gorgeous', self.spellchecker.check_word('gorgeus'))

    def test_simple_nearest(self):
        self.assertIn('loaf', self.spellchecker.get_nearest('loah'))
        self.assertIn('load', self.spellchecker.get_nearest('loah'))
        self.assertIn('misspelling', self.spellchecker.get_nearest('mispeling'))

    def test_sentence_when_can_correct(self):
        self.assertEqual('my sentence have multiple mistakes',
                         self.spellchecker.check_sentence('my ssentense have multipli mistackes'))
        self.assertEqual('another sentence corrupted with mistakes',
                         self.spellchecker.check_sentence('anothher sentence corupted with mistakes'))

    def test_sentence_when_no_matching(self):
        self.assertEqual('my centensse corupptet',
                         self.spellchecker.check_sentence('my centensse corupptet'))

    def test_correcting(self):
        words = ['diplomatically', 'disadvantageous', 'disallowing', 'hollowed', 'incrimination']
        corrupted = ['diplomaticaly', 'dizadvantageus', 'disalowin', 'holowed', 'incremination']

        self.assertEqual(words, [self.spellchecker._correct(w) for w in corrupted])


class Spelling_Tests(unittest.TestCase):

    def setUp(self) -> None:
        words = []
        with open("en-base.txt", 'r') as base:
            words = set(re.findall(r'\w+', base.read().lower()))

        alphabet = "abcdefghijklmnopqrstuvwxyz"

        self.spellchecker = Spellchecker(words, alphabet)
        self.spelling = Spelling('mistacke', self.spellchecker)

    def test_levenstein(self):
        self.assertEqual(0, Spelling.levenstein('spelling', 'spelling'))
        self.assertEqual(1, Spelling.levenstein('speling', 'spelling'))
        self.assertEqual(1, Spelling.levenstein('biba', 'boba'))
        self.assertEqual(2, Spelling.levenstein('австрия', 'австралия'))
        self.assertEqual(3, Spelling.levenstein('котик', 'скотина'))
        self.assertEqual(5, Spelling.levenstein('гибралтар', 'лабрадор'))

    def test_empty_matching_list(self):
        words = ['dfgfdg', 'rgrbfdgdr', 'dfgdfgdg', 'nonmatching', 'mistacke']
        self.assertTrue(len(self.spelling.match_known(words)) == 0)

    def test_itself_when_no_nearest(self):
        words = ['dfgfdg', 'rgrbfdgdr', 'dfgdfgdg']
        spellings = [Spelling(w, self.spellchecker) for w in words]
        self.assertEqual(words, [spelling.nearest_candidates()[0] for spelling in spellings])
