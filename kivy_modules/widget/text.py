from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.codeinput import CodeInput
from kivy.metrics import sp

from kivy.properties import (
    StringProperty, ListProperty, NumericProperty
)

try:
    from kivy_modules.icons import md_icons
    from kivy_modules.behavior.textbehavior import Prettify
except:
    import sys
    path = os.path.dirname(os.path.dirname(resource_find(".")))
    sys.path.insert(0, path)
    from kivy_modules.icons import md_icons

class AutoComplete(TextInput):
    background_color = ListProperty([1,1,1,1])
    source = [
        "ActionScript", "AppleScript", "Asp", "BASIC", "C", "C++",
        "Clojure", "COBOL", "ColdFusion", "Erlang", "Fortran",
        "Groovy", "Haskell", "Java", "JavaScript", "Lisp", "Perl",
        "PHP", "Python", "Ruby", "Scala", "Scheme"
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.start)

    def start(self, *args):
        pass

class FlatText(TextInput):
    text = StringProperty("")
    border_color = ListProperty([0.0,0.4471,0.8235,1])
    border_weigth = NumericProperty(1)
    radius = ListProperty([10])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = [0,0,0,0]
        self.background_normal = ''
        self.background_active = ''
        #self.color = [1,0,0,1] #[0.0, 0.4471, 0.8235, 1]
        self.font_size = sp(20)
        self.bg_color = [0, 0, 1, 1]
        self.cursor_color = [0, 0, 1, 1]
        self.halign = 'center'
        self.valign = 'middle'
        self.hint_text_color = [0.0, 0.4471, 0.8235, .5]
        self.foreground_color = [0.0, 0.4471, 0.8235, 1]
        self.background_color = [0,0,0,0]

        self.text = kwargs.get("text", self.text)
        self.border_color = kwargs.get("border_color", self.border_color)
        self.border_weigth = kwargs.get("border_weigth", self.border_weigth)
        self.radius = kwargs.get("radius", self.radius)

class FlexText(TextInput):
    font_size = NumericProperty(sp(15))
    radius = ListProperty([10,])
    border_weigth = NumericProperty(1)

    bg_normal_color = ListProperty([1,1,1,1])
    bg_active_color = ListProperty([.98,.98,1,1])
    border_normal_color = ListProperty([.1,.1,.1,1])
    border_active_color = ListProperty([0.0, 0.4471, 0.8235, 1])
    hint_text_color = ListProperty([.3,.3,.3,1])
    cursor_color = ListProperty([0.0, 0.4471, 0.8235, 1])
    fg_color = ListProperty([.1,.1,.1,1])
    disabled_fg_color = ListProperty([1,.5,0,1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class FlexPrettyText(FlexText, Prettify):
    pass

class FlexPrettyCode(CodeInput, Prettify):
    pass

Builder.load_string('''
<-FlexText>:
    canvas.before:
        Color:
            rgba: self.bg_active_color if self.focus else self.bg_normal_color
        RoundedRectangle:
            radius: self.radius
            pos: self.pos
            size: self.size
        Color:
            rgba:
                (self.cursor_color
                if self.focus and not self._cursor_blink
                else (0, 0, 0, 0))
        RoundedRectangle:
            radius: self.radius
            pos: self._cursor_visual_pos
            size: root.cursor_width, -self._cursor_visual_height
        Color:
            rgba:
                (self.disabled_fg_color \
                 if self.disabled \
                  else (self.hint_text_color if not self.text else self.fg_color))
    canvas.after:
        Color:
            rgba: 
                (self.border_active_color
                if self.focus and not self._cursor_blink
                else self.border_normal_color)
        Line:
            # points: self.x + 20, self.y, self.x + self.width - 20, self.y
            rounded_rectangle: [self.x, self.y, self.width, self.height, *self.radius]
            width: root.border_weigth

<FlexPrettyText>:
    # text_size: root.size

<FlatText>:
    canvas.before:
        Color:
            rgba: root.bg_color if self.focus else root.border_color 
        Line:
            points: self.x + 20, self.y, self.x + self.width - 20, self.y
            width: root.border_weigth

    # ~ canvas.before:
        # ~ Clear
        # ~ Color:
            # ~ rgba: root.border_color
        # ~ RoundedRectangle:
            # ~ pos: root.pos
            # ~ size: root.size
            # ~ radius: root.radius
        
        # ~ Color:
            # ~ rgba: self.border_color
        # ~ Rectangle:
            # ~ #texture: root.texture
            # ~ size: root.size
            # ~ pos: root.pos

        # ~ Color:
            # ~ rgba: root.bg_color
        # ~ RoundedRectangle:
            # ~ pos: [(root.pos[0] + (root.border_weigth / 2)), (root.pos[1] + (root.border_weigth / 2))]
            # ~ size: [(root.size[0] - root.border_weigth), (root.size[1] - root.border_weigth)]
            # ~ radius: root.radius
    # ~ canvas.after:
        # ~ Color:
            # ~ rgba: [0,0,0,1]

<AutoComplete>:
    radius: [0,]
    border_color: [.3, .3, .3, 1]
    border_size: 1
    font_color: [0,0,0,1]
    cursor_color: [0,0,0,1]
    canvas.before:
        Color:
            rgba: root.border_color
        RoundedRectangle:
            pos: root.pos
            size: map(lambda x: x + root.border_size, root.size)
            radius: root.radius
        Color:
            rgba: root.background_color
        RoundedRectangle:
            pos: root.pos
            size: root.size
            radius: root.radius
        Color:
            rgba: root.font_color
        Color:
            rgba: root.cursor_color

<FlexPrettyCode>:
''')

if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout

    class TextApp(App):
        def build(self):
            text = ["hello","world"]*10
            box = BoxLayout(orientation="vertical")
            box.add_widget(FlexText(text=str(text)))
            box.add_widget(FlatText(text=str(text)))
            box.add_widget(AutoComplete(text=str(text)))
            box.add_widget(FlexPrettyText(data=text))
            box.add_widget(FlexPrettyCode(data=text))
            return box
    
    TextApp().run()