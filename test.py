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
                        print(f'{v1} same position and correct')
                        y.append('same position and correct')
                    elif l[0] == "present":
                        print(f'{v1} same position and present')
                        y.append('same position and present')
                except:
                     print('not in present')
                     y.append('not in present')
            else:
                print(f'{v1} not same position')
                y.append('not same position')
        
    
    return y.count("same position and present")>0

again = {
    "i":["correct",1],
    "g":["present",2],
    "h":["present",3],
    "t":["present",4],
}

def create_check(word,evaluation):
    ww = {}
    for i,(w,e) in enumerate(zip(word,evaluation)):
        ww[w]=[e,i]
    
    return ww

print(check_word("light","girth",again))


