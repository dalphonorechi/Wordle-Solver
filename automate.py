from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time, utils


class Wordle:
    """
    Deals with the UI. Opening the website and automating through the HTML.
    It uses selenium package for automation.
    """

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        s = "C:\\Users\\Hp Pavilion\\Downloads\\Compressed\\chromedriver_win32_2\\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=s, options=chrome_options)
        self.inner_components = None

    def open_wordle(self):
        self.driver.maximize_window()
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")

    def get_game_elements(self):
        time.sleep(15)
        self.inner_components = self.driver.execute_script(
            """return document.querySelector('game-app').shadowRoot.querySelector('game-theme-manager').querySelector('game-keyboard').shadowRoot.querySelector('#keyboard')"""
        )

    def close_dialog(self):
        close_dialog = self.driver.execute_script(
            """return document.querySelector('game-app').shadowRoot.querySelector('game-theme-manager').querySelector('game-modal').shadowRoot.querySelector('.overlay').querySelector('.content').querySelector('.close-icon')"""
        )
        close_dialog.click()

    def press_enter(self):
        enter = self.inner_components.find_elements(
            By.XPATH, ".//div//button[@data-key='↵']"
        )[0]
        enter.click()

    def press_delete(self):
        back = self.inner_components.find_elements(
            By.XPATH, ".//div//button[@data-key='←']"
        )[0]
        back.click()

    def check_word_in_list(self):
        """Checks if selected word is not in the wordle 'list' and deletes it."""
        try:
            game_toast = self.driver.execute_script(
                """return document.querySelector('game-app').shadowRoot.querySelector('game-theme-manager').querySelector('#game').querySelector('#game-toaster')"""
            )
            toast = game_toast.find_element(By.XPATH, ".//game-toast").get_attribute(
                "text"
            )
            print(toast)

            if toast == "Not in word list":
                return True
            else:
                return False
        except:
            return False

    def type_word(self, word):
        for i in word:
            inner = self.inner_components.find_elements(
                By.XPATH, f".//div//button[@data-key='{i}']"
            )[0]
            time.sleep(2)
            inner.click()

    def expand_shadow_element(self, element):
        shadow_root = self.driver.execute_script(
            'return arguments[0].shadowRoot.querySelector("div")', element
        )
        return shadow_root

    def check_evaluation(self, track):
        """
        Checks the position of letters if they are correct,present,or absent in the word.
        """
        game_board = self.driver.execute_script(
            """return document.querySelector('game-app').shadowRoot.querySelector('game-theme-manager').querySelector('#board-container').querySelector('#board').querySelectorAll('game-row')"""
        )
        for i in range(0, 5):
            eval = (
                self.expand_shadow_element(game_board[track.tries]).find_elements(
                    By.XPATH, ".//game-tile"
                )[i]
            ).get_attribute("evaluation")
            letter = (
                self.expand_shadow_element(game_board[track.tries]).find_elements(
                    By.XPATH, ".//game-tile"
                )[i]
            ).get_attribute("letter")
            track.evaluations.append(eval)
            track.letters.append(letter)

    def check_word_in_list_and_delete(self, track):
        if self.check_word_in_list():
            for i in range(0, 5):
                time.sleep(2)
                self.press_delete()

            utils.guessed_not.append(track.guessed.upper())

            track.guessed = "shore"
            return True
        else:
            return False
