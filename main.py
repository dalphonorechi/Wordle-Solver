import time
import api, utils
from automate import Wordle
from track import Track

wordle = Wordle()

track = Track()

wordle.open_wordle()

wordle.get_game_elements()

wordle.close_dialog()

while track.tries < 6 or track.evaluations.count("correct") != 5:

    wordle.type_word(word=track.guessed)

    print(track.guessed)

    wordle.press_enter()
    time.sleep(5)

    isThere = wordle.check_word_in_list()

    if isThere == True:
        for i in range(0, 5):
            time.sleep(2)
            wordle.press_delete()

        utils.guessed_not.append(track.guessed.upper())

        track.guessed = api.get_word(
            api.get_patterns(track)[1], api.get_patterns(track)[0]
        )

        continue

    track.reset_letters()

    wordle.check_evaluation(track)

    track.sort_evaluations()

    track.build_correct_string()

    temp_c = api.get_words(track)

    track.get_guess(temp_c=temp_c)

    track.reset_evaluation()

    track.update_tries()

time.sleep(25)
