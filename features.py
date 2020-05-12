import webbrowser
from spellchecker import SpellChecker


def openWebsite(website):
    webbrowser.open('https://www.' + website + '.com/', new=0)

def spellcheck(str):
    spell = SpellChecker()
    strWordList = str.split()

    for i in range(len(strWordList)):
        word = strWordList[i]
        if spell.unknown([word]):
            strWordList[i] = spell.correction(word)
    
    str = " ".join(strWordList)
    return str