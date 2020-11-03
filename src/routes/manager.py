from src.helpers.imports import *
from src.styles.style import *
from src.pages import *

class Manager(ScreenManager):
    pass

Builder.load_string("""
<Manager>:
    Home:
        name: "home"
    Wordboard:
        name: "wordboard"
    Study:
        name: "study"
    Lang1:
        name: "lang1"
    Lang2:
        name: "lang2"
""")
