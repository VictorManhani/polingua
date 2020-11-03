from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.resources import resource_find
from kivy.core.window import Window
Window.size = (800,500)

import sys
sys.path.insert(0, resource_find('.'))

# from kivy_modules.widget import *

from kivy_modules.widget.button import FlexButton, IconButton
from kivy_modules.widget.calendar import FlexCalendar
from kivy_modules.widget.gradient import ButtonGradient, LabelGradient
from kivy_modules.widget.label import FlexLabel
from kivy_modules.widget.layout import FlexLayout
from kivy_modules.widget.message import SaveMessage
from kivy_modules.widget.progressbar import CircularProgressBar, TrackLoadProgressBar
from kivy_modules.widget.slider import FlexSlider
from kivy_modules.widget.spinner import FlexSpinner
from kivy_modules.widget.tablayout import TabLayout, TabItem
from kivy_modules.widget.table import FlexTable
from kivy_modules.widget.text import FlexText
from kivy_modules.widget.toast import Toast
from kivy_modules.widget.togglebutton import FlexToggleButton
from kivy_modules.widget.tooltip import Tooltip
from kivy_modules.widget.widget import FlexWidget
from kivy_modules.widget.navigation import StackNavigator, BottomNavigator

"""TO CALL THE RELOADER YOU NEED TO CALL IN TERMINAL FROM THE ROOT PATH OF YOUR PROJECT:

py kivy_modules/utils/main.py

"""

KV = '''
#:import KivyLexer kivy.extras.highlight.KivyLexer
#:import HotReloadViewer reload_viewer.HotReloadViewer

BoxLayout:
    CodeInput:
        lexer: KivyLexer()
        style_name: "native"
        on_text: app.update_kv_file(self.text)
        size_hint_x: .7

    HotReloadViewer:
        size_hint_x: .3
        path: app.path_to_kv_file
        errors: True
        errors_text_color: 1, 1, 0, 1
        errors_background_color: app.theme_cls.bg_dark
'''

class Example(MDApp):
    path_to_kv_file = resource_find("my.kv")
    print(path_to_kv_file)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def update_kv_file(self, text):
        with open(self.path_to_kv_file, "w") as kv_file:
            kv_file.write(text)

Example().run()