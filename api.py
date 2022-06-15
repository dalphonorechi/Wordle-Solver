import requests
from json import loads
import random as rn
import utils


class Api:
    def get_word(self, correct="?????", pattern_not="", pattern=""):

        response = requests.get(
            f"https://api.datamuse.com/words?sp={correct}{pattern_not}{pattern}"
        )
        words = []

        for i in loads(response.text):
            words.append(i["word"])
        t = 0
        g = rn.choice(words)
        while utils.guessed_not.count(g) > 0:
            g = rn.choice(words)
            t += 1

        return g

    def check_word(self, wo, gu, against):
        w = list(wo)
        g = list(gu)
        same_position = []
        y = []

        for i, (v1, v2) in enumerate(zip(w, g)):
            if v1 == v2:
                try:
                    l = against[v1]
                    if l[0] == "correct":
                        # print(f'{v1} same position and correct')
                        y.append("same position and correct")
                    elif l[0] == "present":
                        # print(f'{v1} same position and present')
                        y.append("same position and present")
                except:
                    # print('not in present')
                    y.append("not in present")
            else:
                # print(f'{v1} not same position')
                y.append("not same position")

        return y.count("same position and present") > 0

    def get_patterns(self, track):
        pattern = ""
        for i in track.present:
            pattern = pattern + f",*{i}*"

        pattern_absent = "-"
        for i in track.absent:
            pattern_absent = pattern_absent + f"{i}"

        return [pattern, pattern_absent]

    def get_words(self, track):
        """
        Returns wordlist based on the correct,absent and present positions.
        It makes an api call to [datamuse.com] using wild cards.
        """
        print(track.correct)

        pattern = self.get_patterns(track)[0]

        pattern_absent = self.get_patterns(track)[1]

        response = requests.get(
            f"https://api.datamuse.com/words?sp={track.correct}{pattern_absent}{pattern}"
        )
        words = []
        for i in loads(response.text):
            words.append(i["word"])

        temp_c = words.copy()
        for k in words:
            b = self.check_word(
                k, track.guessed, self.create_check(track.guessed, track.evaluations)
            )
            if b:
                temp_c.remove(k)

        return temp_c

    def create_check(self, word, evaluation):
        ww = {}
        for i, (w, e) in enumerate(zip(word, evaluation)):
            ww[w] = [e, i]

        return ww
