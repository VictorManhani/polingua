main = """\
from kivy.core.window import Window
from kivy.utils import platform

if platform not in ["android", "ios"]:
    Window.size = (350,500)

from src.helpers.imports import *

from src.routes.manager import Manager

class TemplateApp(App):
    title = "Template"

    @mainthread
    def switch_screen(self, screen, direction):
        self.root.transition.direction = direction
        self.root.current = screen

    def build(self):
        return Manager()

TemplateApp().run()
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

init_simple = """\
from .home import Home

__all__ = ("Home",)
"""

home_simple = """\
from src.helpers.imports import *

class Home(Screen):
    pass

Builder.load_string(\"\"\"
<Home>:
    FlexLayout:
        padding: [10,30]
        FlexButton:
            text: "Hello World"
            on_release:
                print(self.text)
\"\"\")
"""

manager_simple = """\
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
         "__init__": [init_simple, "pages"], 
         "home":  [home_simple, "pages"], 
         "manager": [manager_simple, "routes"]}