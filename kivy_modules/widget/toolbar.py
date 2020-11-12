from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

from kivy.properties import (
    ListProperty, NumericProperty, StringProperty, 
    OptionProperty, BooleanProperty
)
from kivy.metrics import sp, dp

from kivy.resources import resource_find
import os

try:
    from kivy.uix.boxlayout import BoxLayout
    from ..widget.button import IconButton
    from ..widget.button import FlexButton
    from ..widget.label import FlexLabel
    from ..widget.layout import FlexLayout
except:
    import sys
    path = os.path.dirname(os.path.dirname(resource_find(".")))
    sys.path.insert(0, path)

    from kivy_modules.widget.button import IconButton
    from kivy_modules.widget.button import FlexButton
    from kivy_modules.widget.label import FlexLabel
    from kivy_modules.widget.layout import FlexLayout

from kivy_modules.icons import md_icons

from functools import partial

class FlexToolbar(BoxLayout):
    # RESETS
    orientation = StringProperty("horizontal")
    bg_color = ListProperty([1,.5,0,1])
    source = StringProperty("")
    padding = ListProperty([0,0,0,0])
    spacing = dp(0)

    # ATRIBUTTES
    title = StringProperty("")

    previous_screen = StringProperty("")
    first_button_icon = StringProperty("arrow-left")
    first_button_text = StringProperty("")
    first_button_disabled = BooleanProperty(False)
    first_button_callback = None # lambda parent: print("<- First Button", parent)

    next_screen = StringProperty("")
    second_button_text = StringProperty("")
    second_button_icon = StringProperty("arrow-right")
    second_button_disabled = BooleanProperty(False)
    second_button_callback = None # lambda parent: print("Second Button ->", parent)

    # COLORS
    title_color = ListProperty([1,1,1,1])
    first_button_color = ListProperty([.1,.1,.1,1])
    second_button_color = ListProperty([.1,.1,.1,1])

    # SIZES
    button_size_x = dp(.15)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.start)

    def start(self, evt):
        self.app = App.get_running_app()

        if self.first_button_icon:
            icon = self.create_icon_button(
                self.first_button_icon, self.first_button_color,
                self.first_button_disabled,
                self.first_button_callback, self.previous_screen
            )
            self.add_widget(icon)
        elif self.first_button_text:
            but = self.create_text_button(
                self.first_button_text, self.first_button_color, 
                self.first_button_disabled,
                self.first_button_callback, self.previous_screen
            )
            self.add_widget(but)

        label = FlexLabel(
            text = self.title,
            size_hint_x = 1. - (2 * self.button_size_x),
            markup = True, 
            outline_width = sp(1),
            color = self.title_color,
            bold = True,
            outline_color = [.2,.2,.2,1]
        )

        self.add_widget(label)

        if self.second_button_icon:
            but = self.create_icon_button(
                self.second_button_icon, 
                self.second_button_color,
                self.second_button_disabled,
                self.second_button_callback, self.next_screen
            )
            self.add_widget(but)
        elif self.second_button_text:
            but = self.create_text_button(
                self.second_button_text, 
                self.second_button_color,
                self.second_button_disabled,
                self.second_button_callback, self.next_screen
            )
            self.add_widget(but)

    def func(self, button_callback, screen, direction, obj):
        if button_callback:
            button_callback()
        else:
            self.app.switch_screen(screen, direction)

    def create_icon_button(
        self, button_icon, fg_color, button_disabled, button_callback, screen):
        but = IconButton(
            icon = button_icon, size_hint_x = self.button_size_x
        )
        but.disabled = button_disabled
        but.icon_color = [0,0,0,0] if but.disabled else fg_color
        but.color = [0,0,0,0] if but.disabled else fg_color
        but.fg_color = [0,0,0,0] if but.disabled else fg_color      
        but.border_color = [0,0,0,0] if but.disabled else but.border_color
        but.bg_color = [0,0,0,0] if but.disabled else but.bg_color
        but.bg_color_normal = [0,0,0,0] if but.disabled else but.bg_color_normal
        but.bg_color_press = [0,0,0,0] if but.disabled else but.bg_color_press

        but.bind(on_release = partial(self.func, button_callback, screen, "right"))

        return but

    def create_text_button(
        self, button_text, fg_color, button_disabled, button_callback, screen):
        but = FlexButton(
            text = button_text, size_hint_x = self.button_size_x
        )
        but.disabled = button_disabled
        but.fg_color = [0,0,0,0] if but.disabled else fg_color
        but.color = [0,0,0,0] if but.disabled else fg_color
        but.border_color = [0,0,0,0] if but.disabled else but.border_color
        but.bg_color = [0,0,0,0] if but.disabled else but.bg_color
        but.bg_color_normal = [0,0,0,0] if but.disabled else but.bg_color_normal
        but.bg_color_press = [0,0,0,0] if but.disabled else but.bg_color_press

        but.bind(on_release = partial(self.func, button_callback, screen, "left"))

        return but

Builder.load_string("""
<FlexToolbar>:
""")

if __name__ == "__main__":
    class FlexToolbarApp(App):
        def build(self):
            flexlayout = FlexLayout()
            flextoolbar = FlexToolbar(
                size_hint = [1,.1],
                title = "Test"
            )
            flexlabel = FlexLabel(size_hint = [1,.9])
            flexlayout.add_widget(flextoolbar)
            flexlayout.add_widget(flexlabel)
            return flexlayout

    FlexToolbarApp().run()