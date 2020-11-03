main = """\
from kivy.core.window import Window
from kivy.utils import platform

if platform not in ["android", "ios"]:
    Window.size = (350,500)

from src.helpers.imports import *

from src.routes.manager import Manager

class MapApp(App):
    title = "Map Template"

    @mainthread
    def switch_screen(self, screen, direction):
        self.root.transition.direction = direction
        self.root.current = screen

    def build(self):
        return Manager()

MapApp().run()
"""

imports = """\
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.uix.screenmanager import Screen, ScreenManager

from kivy_modules.widget.layout import FlexLayout
from kivy_modules.widget.button import FlexButton
from kivy_modules.widget.label import FlexLabel

__all__ = ("App", "Builder", "Clock", "mainthread",
           "ScreenManager", "Screen",

           "FlexLayout", "FlexButton",)
"""

init = """\
from .home import Home

__all__ = ("Home",)
"""

home = """\
from src.helpers.imports import *

class Home(Screen):
    pass

Builder.load_string(\"\"\"
<Home>:
    FlexLayout:
        padding: [10,30]
        FlexLabel:
            text: "Map"
            size_hint: [1,.1]
        FlexButton:
            text: "Get Map"
            size_hint: [1,.9]
            on_release:
                print("Map")
\"\"\")
"""

manager = """\
from src.helpers.imports import *
from src.pages import *

class Manager(ScreenManager):
    pass

Builder.load_string(\"\"\"
<Manager>:
    Home:
        name: "home"
\"\"\")
"""

parts = {"main": [main, "current_work"], 
         "imports": [imports, "helpers"], 
         "__init__": [init, "pages"], 
         "home":  [home, "pages"], 
         "manager": [manager, "routes"]}