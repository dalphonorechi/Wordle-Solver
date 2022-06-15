import utils
from api import Api


class Track:
    """
    Keeps Track of the letters positions and if they correct,present or absent.
    """

    def __init__(self):
        self.api = Api()
        self.tries = 0
        self.evaluations = []
        self.present = []
        self.absent = []
        self.correct = "?????"
        self.indices = []
        self.correct_list = []
        self.letters = []
        self.guessed = self.api.get_word()

    def all_evaluations_correct(self):
        return self.evaluations.count("correct") == 5

    def sort_evaluations(self):
        for i in range(len(self.evaluations)):
            if self.evaluations[i] == "correct":
                self.indices.append(i)
                self.correct_list.append(self.letters[i])
            elif self.evaluations[i] == "present":
                if self.present.count(self.letters[i]) == 0:
                    self.present.append(self.letters[i])
            else:
                if (
                    self.correct_list.count(self.letters[i]) == 0
                    or self.present.count(self.letters[i]) == 0
                ):
                    self.absent.append(self.letters[i])

    def build_correct_string(self):
        """
        Builds correct string with postions that ar correct e.g ??e?t.
        """
        temp = list(self.correct)
        for i in self.indices:
            temp[i] = self.letters[i]

        self.correct = "".join(temp)

    def get_guess(self, temp_c):
        print(temp_c)
        try:
            utils.guessed_not.append(self.guessed.upper())
            self.guessed = self.pick_word(temp_c, g=utils.guessed_not)
        except:

            self.guessed = self.api.get_word(
                correct=self.correct,
                pattern=self.api.get_patterns(self)[1],
                pattern_not=self.api.get_patterns(self)[0],
            )

    def pick_word(self, list_choice, g):
        t = 0
        guess = list_choice[0]
        while g.count(guess.upper()) > 0:
            guess = list_choice[t]
            t += 1
        return guess

    def reset_letters(self):
        self.letters = []

    def reset_evaluation(self):
        self.evaluations = []

    def update_tries(self):
        self.tries += 1
