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
        self.inner_components = self.driver.execute_script(
            """return document.querySelector('#wordle-app-game').querySelector('.Keyboard-module_keyboard__1HSnn')"""
        )

    def close_dialog(self):
        close_dialog = self.driver.execute_script(
            """return document.querySelector('#wordle-app-game').querySelector('.Modal-module_modalOverlay__81ZCi').querySelector('.Modal-module_content__s8qUZ').querySelector('.Modal-module_closeIcon__b4z74')"""
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
                """return document.querySelector('#wordle-app-game').querySelector('.ToastContainer-module_toaster__QDad3')"""
            )
            print(game_toast.get_attribute("innerHTML"))

            toast = game_toast.find_element(By.XPATH, ".//div").get_attribute(
                "innerHTML"
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

    # def expand_shadow_element(self, element):
    #     shadow_root = self.driver.execute_script(
    #         'return arguments[0].shadowRoot.querySelector("div")', element
    #     )
    #     return shadow_root

    def check_evaluation(self, track):
        """
        Checks the position of letters if they are correct,present,or absent in the word.
        """
        game_board = self.driver.execute_script(
            """return document.querySelector('#wordle-app-game').querySelector('.Board-module_boardContainer__cKb-C').querySelector('.Board-module_board__lbzlf').querySelectorAll('.Row-module_row__dEHfN')"""
        )
        time.sleep(2)

        for i in range(0, 5):
            eval = game_board[track.tries].find_elements(By.XPATH, ".//div//div")[i].get_attribute("data-state")
            letter = game_board[track.tries].find_elements(By.XPATH, ".//div//div")[i].get_attribute("innerHTML")

            track.evaluations.append(eval)
            track.letters.append(letter)

        print("Printing evaluations")
        print(track.evaluations)
        print(track.letters)

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

    def close_wordle(self):
        self.driver.quit()
