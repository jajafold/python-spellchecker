class Tokenizer:

    @staticmethod
    def tokenize(text: str) -> list:
        result = []
        word = ''

        for sym in text:
            if not sym.isalpha() and sym != '-':
                if word != '':
                    result.append(word)
                    word = ''

                result.append(sym)
            else:
                word += sym

        return result

