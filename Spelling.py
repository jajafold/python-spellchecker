class Spelling:

    def __init__(self, word: str, checker):
        self.word = word
        self.checker = checker

    @staticmethod
    def levenstein(str_1, str_2):
        n, m = len(str_1), len(str_2)
        if n > m:
            str_1, str_2 = str_2, str_1
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if str_1[j - 1] != str_2[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]

    def correct(self):
        return min([(Spelling.levenstein(self.word, w), w) for w in self.nearest_candidates()])[1]

    def nearest_candidates(self) -> set:
        _nearest = set()
        _nearest.update(self.edit1(self.word))
        _nearest.update(self.edit2(self.word))

        return self.match_known(_nearest) or [self.word]

    def match_known(self, words) -> set:
        return set([candidate for candidate in words if candidate in self.checker.known_words])

    def edit1(self, word) -> set:
        alphabet = self.checker.alphabet
        split = [(word[:i], word[i:]) for i in range(len(word) + 1)]

        delete = [left + right[1:] for left, right in split if right]
        transpose = [left + right[:2][::-1] + right[2:] for left, right in split if len(right) > 1]
        replace = [left + replace_character + right[1:] for left, right in split for replace_character in alphabet if right]
        insert = [left + insert_character + right[0:] for left, right in split for insert_character in alphabet]

        return set(delete + transpose + replace + insert)

    def edit2(self, word):
        return (e2 for e1 in self.edit1(word) for e2 in self.edit1(e1))
