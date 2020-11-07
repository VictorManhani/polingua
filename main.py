from kivy.core.window import Window
from kivy.utils import platform

if platform not in ["android", "ios"]:
    Window.size = (350,500)

from src.helpers.imports import *

from src.routes.manager import Manager

from src.helpers.helpers import reproduce

class PolinguaApp(App):
    title = "Polingua"
    store = None
    font_size = sp(15)
    style_color = {
        "ripple_color": [1,.6,.6,1],
        "first_body_color": [1,.5,.5,1],
        "second_body_color": [1,1,1,1],
        "terciary_body_color": [1,.7,.7,1],
        "quarter_body_color": [.95,.95,.95,1],
        "fifth_body_color": [.2,.8,1,.2],
        "first_font_color": [.2,.2,.2,1],
        "second_font_color": [1,1,1,1]
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = MStore()
        # os.path.dirname(os.path.abspath(__file__))
        self.store.store_load(os.path.join("src", "databases", "words.json"))

    @mainthread
    def switch_screen(self, screen, direction, transition=None):
        if transition:
            self.root.transition = globals()[transition]()
        else:
            self.root.transition.direction = direction
        self.root.current = screen

    def reproduce(self, text, lang):
        reproduce(text, lang)

    def build(self):
        return Manager()

PolinguaApp().run()
