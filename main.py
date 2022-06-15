import time
import api, utils
from automate import Wordle
from track import Track
from api import Api

wordle = Wordle()

track = Track()

api = Api()

wordle.open_wordle()

wordle.get_game_elements()

wordle.close_dialog()

while track.tries < 6 or not track.all_evaluations_correct():

    wordle.type_word(word=track.guessed)

    wordle.press_enter()

    if wordle.check_word_in_list_and_delete(track):
        continue

    track.reset_letters()

    wordle.check_evaluation(track)

    track.sort_evaluations()

    track.build_correct_string()

    if track.all_evaluations_correct():
        print("exiting")
        break

    temp_c = api.get_words(track)

    track.get_guess(temp_c=temp_c)

    track.reset_evaluation()

    track.update_tries()

time.sleep(25)
