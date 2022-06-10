from urllib import response
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import requests
from json import loads

def pick_word(list_choice,g):
    t=0
    guess = list_choice[0]
    while(g.count(guess.upper()) > 0):
        guess=list_choice[t]
        t+=1
    return guess

def check_word(wo,gu,against):
    w= list(wo)
    g= list(gu)
    same_position = []
    y =[]
    
    for i,(v1,v2) in enumerate(zip(w,g)):
            if v1 == v2:
                try:
                    l = against[v1]
                    if l[0] == "correct":
                        #print(f'{v1} same position and correct')
                        y.append('same position and correct')
                    elif l[0] == "present":
                        #print(f'{v1} same position and present')
                        y.append('same position and present')
                except:
                     #print('not in present')
                     y.append('not in present')
            else:
                #print(f'{v1} not same position')
                y.append('not same position')
        
    
    return y.count("same position and present")>0


def create_check(word,evaluation):
    ww = {}
    for i,(w,e) in enumerate(zip(word,evaluation)):
        ww[w]=[e,i]
    
    return ww


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
s = "C:\\Users\\Hp Pavilion\\Downloads\\Compressed\\chromedriver_win32_2\\chromedriver.exe"
driver = webdriver.Chrome(executable_path=s,options=chrome_options)
driver.maximize_window()
driver.get("https://www.nytimes.com/games/wordle/index.html")
time.sleep(5)

def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot.querySelector("div")', element)
  return shadow_root


inner_text = driver.execute_script("""return document.querySelector('game-app').shadowRoot.querySelector('game-theme-manager').querySelector('game-keyboard').shadowRoot.querySelector('#keyboard')""")
# for i in inner_text:
# k = []
# for p in inner_text:
#     l = p.find_elements(By.XPATH,f".//button")
#     k.append(l)
tries = 0
guessed = "least"
guessed_not=["TRAIT","FLOOD","GLOOM","DEPTH","FROTH","PEACH","SHOWY","CREAK","MANOR","ATOLL","BAYOU","CREPT","TIARA","ASSET","VOUCH","ALBUM","HINGE","MONEY","SCRAP","GAMER","GLASS","SCOUR","BEING","DELVE","YIELD","METAL","TIPSY","SLUNG","FARCE","GECKO","SHINE","CANNY","MIDST","BADGE","HOMER","TRAIN","HAIRY","STORY","FORGO","LARVA","TRASH","ZESTY","SHOWN","HEIST","ASKEW","INERT","OLIVE","PLANT","OXIDE","CARGO","FOYER","FLAIR","AMPLE","CHEEK","SHAME","MINCE","CHUNK","ROYAL","SQUAD","BLACK","STAIR","SCARE","FORAY","COMMA","NATAL","SHAWL","FEWER","TROPE","SNOUT","LOWLY","STOVE","SHALL","FOUND","NYMPH","EPOXY","DEPOT","CHEST","PURGE","SLOSH","THEIR","RENEW","ALLOW","SAUTE","MOVIE","CATER","TEASE","SMELT","FOCUS","TODAY","WATCH","LAPSE","MONTH","SWEET","HOARD","CLOTH","BRINE","AHEAD","MOURN","NASTY","RUPEE","CHOKE","CHANT","SPILL","VIVID","BLOKE","TROVE","THORN","OTHER","TACIT","SWILL","DODGE","SHAKE","CAULK","AROMA","CYNIC","ROBIN","ULTRA","ULCER","PAUSE","HUMOR","FRAME","ELDER","SKILL","ALOFT","PLEAT","SHARD","MOIST","THOSE","LIGHT","WRUNG","COULD","PERKY","MOUNT","WHACK","SUGAR","KNOLL","CRIMP","WINCE","PRICK","ROBOT","POINT","PROXY","SHIRE","SOLAR","PANIC","TANGY","ABBEY","FAVOR","DRINK","QUERY","GORGE","CRANK","SLUMP","BANAL","TIGER","SIEGE","TRUSS"," BOOST"," REBUS",]
correct = "?????"
indices = []
present = []
absent = []
correct_list = []
evaluations = []
while tries < 6 or evaluations.count("correct") != 5:
    for i in guessed:
            inner = inner_text.find_elements(By.XPATH,f".//div//button[@data-key='{i}']")[0]
            time.sleep(2)
            inner.click()

    enter = inner_text.find_elements(By.XPATH,".//div//button[@data-key='↵']")[0]
    enter.click()
    try:
        game_toast = driver.execute_script("""return document.querySelector('game-app').shadowRoot.querySelector('game-theme-manager').querySelector('#game').querySelector('#game-toaster')""")
        toast = game_toast.find_element(By.XPATH,'.//game-toast').get_attribute("text")
        print(f"toast is {toast}")
        back = inner_text.find_elements(By.XPATH,".//div//button[@data-key='←']")[0]
        if(toast == "Not in word list"):
            for i in range(0,5):
                time.sleep(2)
                back.click()
            guessed_not.append(guessed.upper())
            guessed = pick_word(["shore"],g=guessed_not)

            continue
    except:
        print("word in list")

    game_board  = driver.execute_script("""return document.querySelector('game-app').shadowRoot.querySelector('game-theme-manager').querySelector('#board-container').querySelector('#board').querySelectorAll('game-row')""")
    invalid = expand_shadow_element(game_board[tries]).get_attribute("invalid")
    print(f"Is invalid {invalid}")
    letters = []
    for i in range(0,5):
        eval = (expand_shadow_element(game_board[tries]).find_elements(By.XPATH,".//game-tile")[i]).get_attribute("evaluation")
        letter =(expand_shadow_element(game_board[tries]).find_elements(By.XPATH,".//game-tile")[i]).get_attribute("letter")
        evaluations.append(eval)
        letters.append(letter)

    print(evaluations)
    print(letters)
    for i in range(len(evaluations)):
        if evaluations[i] == "correct":
            indices.append(i)
            correct_list.append(letters[i])
        elif evaluations[i] =="present":
            present.append(letters[i])
        else:
            if correct_list.count(letters[i]) == 0 or present.count(letters[i]) == 0:
                absent.append(letters[i])
    temp = list(correct)
    for i in indices:
        temp[i]=letters[i]

    correct = "".join(temp)

    print(correct)
    pattern = ""
    for i in present:
        pattern = pattern + f',*{i}*'

    pattern_absent = "-"
    for i in absent:
        pattern_absent = pattern_absent + f'{i}'
    print(pattern_absent)

    response = requests.get(f"https://api.datamuse.com/words?sp={correct}{pattern_absent}{pattern}")
    words = []
    print()
    print()
    print()
    for i in loads(response.text):
        words.append(i["word"])


    temp_c = words.copy()
    for k in words:
        b = check_word(k,guessed,create_check(guessed,evaluations))
        if b:
            temp_c.remove(k)
        
    print(f"words that fit : {temp_c[:5]}")
    #print(f"all words : {words}")
    guessed_not.append(guessed.upper())
    guessed= pick_word(temp_c,g=guessed_not)
    evaluations.clear()
    tries+=1

time.sleep(5)

