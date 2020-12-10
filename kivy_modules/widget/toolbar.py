from kivy.app import App
from kivy.event import EventDispatcher
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
    from ..widget.button import FlexIconButton
    from ..widget.button import FlexButton
    from ..widget.label import FlexLabel
    from ..widget.layout import FlexBox
    from ..widget.gradient import FlexBoxGradient, FlexGradient
except:
    import sys
    path = os.path.dirname(os.path.dirname(resource_find(".")))
    sys.path.insert(0, path)

    from kivy_modules.widget.button import FlexIconButton
    from kivy_modules.widget.button import FlexButton
    from kivy_modules.widget.label import FlexLabel
    from kivy_modules.widget.layout import FlexLayout
    from kivy_modules.widget.gradient import FlexBoxGradient, FlexGradient

from kivy_modules.icons import md_icons

from functools import partial

class FlexToolbarBase(EventDispatcher):
    # RESETS
    orientation = StringProperty("horizontal")
    bg_color = ListProperty([1,.5,0,1])
    source = StringProperty("")
    padding = ListProperty([0,0,0,0])
    spacing = dp(0)

    # ATRIBUTTES
    title = StringProperty("")

    previous_screen = StringProperty("")
    first_button_icon = StringProperty(None, allowNone=True)
    first_button_text = StringProperty(None, allowNone=True)
    first_button_disabled = BooleanProperty(False)
    first_button_callback = None # lambda parent: print("<- First Button", parent)

    next_screen = StringProperty("")
    second_button_text = StringProperty(None, allowNone=True)
    second_button_icon = StringProperty(None, allowNone=True)
    second_button_disabled = BooleanProperty(False)
    second_button_callback = None # lambda parent: print("Second Button ->", parent)

    # COLORS
    title_color = ListProperty([1,1,1,1])
    first_button_color = ListProperty([.1,.1,.1,1])
    second_button_color = ListProperty([.1,.1,.1,1])
    outline_color = ListProperty([.2,.2,.2,1])

    # SIZES
    button_size_x = dp(.15)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.start)

    def start(self, evt):
        self.app = App.get_running_app()

        self.generate_button("first", self.previous_screen, "right")
        self.generate_title()
        self.generate_button("second", self.next_screen, "left")

    def generate_button(self, order, screen, direction):
        button_icon = getattr(self, f"{order}_button_icon")
        button_color = getattr(self, f"{order}_button_color")
        button_disabled = getattr(self, f"{order}_button_disabled")
        button_callback = getattr(self, f"{order}_button_callback")
        button_text = getattr(self, f"{order}_button_text")

        if button_icon:
            instance = FlexIconButton(icon = button_icon)
            icon = self.create_button(
                instance, button_color, button_disabled,
                button_callback, screen, direction
            )
            self.add_widget(icon)
        elif button_text:
            instance = FlexButton(text = button_text)
            but = self.create_button(
                instance, button_color, button_disabled,
                button_callback, screen, direction
            )
            self.add_widget(but)

    def generate_title(self):
        label = FlexLabel(
            text = self.title,
            size_hint_x = 1. - (2 * self.button_size_x),
            markup = True, outline_width = sp(1),
            color = self.title_color, bold = True,
            outline_color = self.outline_color
        )
        self.add_widget(label)

    def func(self, button_callback, screen, direction, obj):
        if button_callback:
            button_callback()
        else:
            self.app.switch_screen(screen, direction)

    def create_button(
        self, but, fg_color, button_disabled, button_callback, screen, direction):
        but.size_hint_x = self.button_size_x
        but.disabled = button_disabled
        but.icon_color = [0,0,0,0] if but.disabled else fg_color
        but.fg_color = [0,0,0,0] if but.disabled else fg_color      
        but.color = [0,0,0,0] if but.disabled else fg_color
        but.border_color = [0,0,0,0] if but.disabled else but.border_color
        but.bg_color = [0,0,0,0] if but.disabled else but.bg_color
        but.bg_color_normal = [0,0,0,0] if but.disabled else but.bg_color_normal
        but.bg_color_press = [0,0,0,0] if but.disabled else but.bg_color_press
        but.bind(on_release = partial(self.func, button_callback, screen, direction))
        return but

class FlexToolbar(BoxLayout, FlexToolbarBase):
    pass

class FlexToolbarGradient(FlexToolbarBase, FlexBoxGradient):
    pass

Builder.load_string("""
<FlexToolbar>:

<FlexToolbarGradient>:
""")

if __name__ == "__main__":
    class FlexToolbarApp(App):
        def build(self):
            flexbox = FlexBox()
            flextoolbar = FlexToolbar(
                size_hint = [1,.1], title = "Test")
            flextoolbargradient = FlexToolbarGradient(
                size_hint = [1,.1], title = "Test")
            flexlabel = FlexLabel(
                text="Hello World", size_hint = [1,.9])
            flexbox.add_widget(flextoolbar)
            flexbox.add_widget(flextoolbargradient)
            flexbox.add_widget(flexlabel)
            return flexbox

    FlexToolbarApp().run()