from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.metrics import sp
from kivy.properties import (
    StringProperty, ObjectProperty, BooleanProperty,
    NumericProperty, ListProperty
)
from json import dumps
from kivy_modules.behavior.textbehavior import Prettify

class FlexLabel(Label):
    font_size = NumericProperty(sp(15))
    bold = BooleanProperty(False)
    radius = ListProperty([0])
    halign = StringProperty('center')
    valign = StringProperty('middle')

    color = ListProperty([.2,.2,.2,1])
    fg_color = ListProperty([.2,.2,.2,1])
    bg_color = ListProperty([1,1,1,1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fg_color = kwargs.get("fg_color", self.color)
        self.bg_color = kwargs.get("bg_color", self.bg_color)

    def on_fg_color(self, obj, val):
        self.color = val

class FlexPrettyLabel(FlexLabel, Prettify):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ScrollableLabel(ScrollView):
    text = StringProperty('')
    ref_press = ObjectProperty(None)
    markup = BooleanProperty(False)
    __events__ = ['on_ref_press']
    radius = ListProperty([0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # ~ Clock.schedule_once(self.start, .5)
        
    # ~ def start(self, *args):
        # ~ self.children[0].ref_press = on_ref_press

    def on_touch_down(self, touch):
        label = self.children[0]
        if super(Label, label).on_touch_down(touch):
            return True
        if not len(label.refs):
            return False
        
        tx, ty = touch.pos
        tx -= label.center_x - label.texture_size[0] / 2.
        ty -= label.center_y - label.texture_size[1] / 2.
        ty = label.texture_size[1] - ty
        for uid, zones in label.refs.items():
            for zone in zones:
                x, y, w, h = zone
                if x <= tx <= w and y <= ty <= h:
                    self.dispatch('on_ref_press', uid)
                    return True
        return False

    def on_ref_press(self, ref):
        print(ref)

class PrettyLabel(ScrollView):
    """label with a pretty representation of text,
    inspired by pprint module"""
    text = StringProperty('')
    padding = ListProperty([5,5])
    radius = ListProperty([0])
    do_scroll_y = BooleanProperty(True)
    do_scroll_x = BooleanProperty(True)
    # scroll_type = ListProperty(['bars'])
    effect_cls = StringProperty('ScrollEffect')
    bar_width = NumericProperty(10)
    bar_color = ListProperty([.2, .2, 1, 1])
    fg_color = ListProperty([.2, .2, .2, 1])
    bg_color = ListProperty([1,1,1,1])
    orientation = StringProperty("vertical")

    def init(self, *args, **kwargs):
        super(PrettyLabel, self).init(*args, **kwargs)
        self.radius = kwargs.get("radius", self.radius)

    def pprint(self, obj, sort_keys = False, indent = 4):
        """Pretty-print a Python object to a stream [default is sys.stdout]."""
        self.text = dumps(
            obj, sort_keys = sort_keys,
            indent = indent, separators = (',', ': ')
        )

    def write(self, text):
        self.text += text

Builder.load_string('''

<ScrollableLabel>:
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        text: root.text
        markup: True

<FlexLabel>:
    fg_color: root.fg_color
    bg_color: root.bg_color
    text_size: self.size
    canvas.before:
        Color:
            rgba: root.bg_color
        RoundedRectangle:
            pos: root.pos
            size: root.size
            radius: root.radius

<FlexPrettyLabel>:
    text_size: root.size

<PrettyLabel>:
    FlexLabel:
        color: root.fg_color
        size_hint: [None,None]
        size: [0,0]
        width: dp(len(self.text)*2) if root.orientation == "horizontal" else root.width #self.texture_size[0]
        height: dp(len(self.text)) if root.orientation == "vertical" else root.height #self.texture_size[1]
        text_size: [self.width, self.height]
        padding: root.padding
        text: root.text
        markup: True
        canvas.before:
            Color:
                rgba: root.bg_color
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: root.radius
''')

if __name__ == "__main__":
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout

    class LabelApp(App):
        def build(self):
            text = ["hello","world"]*10
            box = BoxLayout(orientation="vertical")
            box.add_widget(FlexLabel(text=str(text)))
            box.add_widget(FlexPrettyLabel(data=text))
            box.add_widget(ScrollableLabel(text=str(text)))
            box.add_widget(PrettyLabel(text=str(text), radius=[30],
                                       orientation="vertical"))
            return box

    LabelApp().run()