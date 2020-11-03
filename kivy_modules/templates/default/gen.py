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

init = """\
from .home import Home
from .splash import Splash

__all__ = ("Home","Splash",)
"""

splash = """\
from src.helpers.imports import *

class Splash(Screen):
    pass

Builder.load_string(\"\"\"
<Splash>:
    FlexLayout:
        padding: [10,30]
        FlexLabel:
            text: "Splash"
            size_hint: [1,.1]
        FlexButton:
            text: "Go To Home"
            size_hint: [1,.9]
            on_release:
                app.switch_screen("home", "left")
\"\"\")
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
            text: "Home"
            size_hint: [1,.1]
        FlexButton:
            text: "Go To Splash"
            size_hint: [1,.9]
            on_release:
                app.switch_screen("splash", "right")
\"\"\")
"""

manager = """\
from src.helpers.imports import *
from src.pages import *

class Manager(ScreenManager):
    pass

Builder.load_string(\"\"\"
<Manager>:
    Splash:
        name: "splash"
    Home:
        name: "home"
\"\"\")
"""

parts = {"main": [main, "current_work"], 
         "imports": [imports, "helpers"], 
         "__init__": [init, "pages"], 
         "home":  [home, "pages"], 
         "splash":  [splash, "pages"], 
         "manager": [manager, "routes"]}