from .imports import *
from plyer import tts

def reproduce(word, lang):
    def run():
        try:
            tts.speak(word)
        except NotImplementedError:
            print("error")

    threading.Thread(target = run).start()