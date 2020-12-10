from kivy.lang import Builder
from kivy.uix.button import Button

from kivy.properties import (
    ListProperty, NumericProperty, StringProperty, 
    OptionProperty, BooleanProperty
)
from kivy.metrics import sp, dp
from kivy.uix.behaviors import TouchRippleBehavior

from kivy.utils import get_hex_from_color
from kivy.resources import resource_find
import os

try:
    from ..behavior.ripplebehavior import CircularRippleBehavior, RectangularRippleBehavior
    from ..behavior.hoverbehavior import HoverBehavior
except:
    import sys
    path = os.path.dirname(os.path.dirname(resource_find(".")))
    sys.path.insert(0, path)
    from kivy_modules.behavior.ripplebehavior import CircularRippleBehavior, RectangularRippleBehavior
    from kivy_modules.behavior.hoverbehavior import HoverBehavior

from kivy_modules.icons import md_icons

class FlatButton(Button):
    radius = ListProperty([0])

class FlexImageButton(Button):
    radius = ListProperty([0])

class FlexButton(RectangularRippleBehavior, Button):
    background_color = [0,0,0,0]
    background_normal = ''
    background_down = ''

    font_size = NumericProperty(sp(20))
    radius = ListProperty([10])
    border_weigth = NumericProperty(dp(1))
    border_width = dp(2)
    ripple_duration_in_fast = 0.2

    color = ListProperty([.2,.2,.2,1]) # foreground color
    fg_color = ListProperty([.2,.2,.2,1]) # background color
    bg_color = ListProperty([1,1,1,1]) # background color
    bg_color_normal = ListProperty([1,1,1,1])
    bg_color_press = ListProperty([.9,.9,.9,1])
    border_color = ListProperty([0.0, 0.4471, 0.8235, 1])
    ripple_color = ListProperty([0.0, 0.6784, 0.9569, 1])

    halign = StringProperty('center')
    valign = StringProperty('middle')

    def __init__(self, **kwargs):
        self.halign = 'center'
        self.valign = 'middle'
        super(FlexButton, self).__init__(**kwargs)
        self.fg_color = kwargs.get("fg_color", self.fg_color)

    def on_fg_color(self, obj, val):
        self.color = val

    def on_press(self, *args):
        self.bg_color = self.bg_color_press

    def on_release(self, *args):
        self.bg_color = self.bg_color_normal

class FlexIconButton(FlexButton):
    markup = BooleanProperty(True)

    kivy_modules = os.path.dirname(
         os.path.dirname(os.path.abspath(__file__)))
    icon_path = resource_find(
         os.path.join(kivy_modules, "font", "icons.ttf"))

    icon = StringProperty('language-python')
    _icon = StringProperty('')

    icon_color = ListProperty([.2,.2,.2,1])
    _icon_color = StringProperty("#000000FF")
    icon_size = NumericProperty(12)

    icon_x = StringProperty('left')

    label = StringProperty('')
    label_font_size = NumericProperty(12)

    def __init__(self, **kwargs):
        super(FlexIconButton, self).__init__(**kwargs)
        self.icon = kwargs.get("icon",self.icon)

    def get_size(self, text):
        start_size = ' [size=' + str(int(self.icon_size)) + ']'
        end_size = '[/size]'
        size = start_size + text + end_size
        return size

    def get_color(self, text):
        start_color = f'[color={self._icon_color}]'
        end_color = '[/color]'
        color = start_color + text + end_color 
        return color

    def get_font(self, text):
        start_font = '[font=' + self.icon_path + ']'
        end_font = '[/font]'
        font = start_font + text + end_font
        return font

    def get_icon(self):
        return md_icons[self.icon]

    def get_label(self, text):
        label = text+self.label \
            if self.icon_x == "left" else self.label + text
        return label

    def on_icon(self, obj, val):
        if self.icon_path:
            self.text = \
                self.get_label(
                    self.get_size(
                        self.get_font(
                            self.get_color(
                                self.get_icon()))))
        else:
            self.text = "?"

    def on_icon_color(self, obj, val):
        self._icon_color = get_hex_from_color(val)

    def on__icon_color(self, obj, val):
        self.on_icon(None, None)

    def on_label(self, obj, val):
        self.on_icon(None, None)

    def on_icon_x(self, obj, val):
        self.on_icon(None, None)
    
    def on_icon_size(self, obj, val):
        self.on_icon(None, None)

    def on_press(self, *args):
        self.bg_color = self.bg_color_press

    def on_release(self, *args):
        self.bg_color = self.bg_color_normal

class FlexButtonDesktop(RectangularRippleBehavior, Button, HoverBehavior):
    hover_color = ListProperty([.6,.8,1,1])
    unhover_color = ListProperty([1,1,1,1])
    ripple_duration_in_fast = 0.2
    background_color = [0,0,0,0]
    background_normal = ''
    background_down = ''
    color = ListProperty([0.0, 0.4471, 0.8235, 1])
    font_size = NumericProperty(sp(20))
    radius = ListProperty([0])
    bg_color = ListProperty([1,1,1,1])
    border_color = ListProperty([0.0, 0.4471, 0.8235, 1])
    border_weigth = NumericProperty(dp(1))
 
    button_type = OptionProperty("rounded", options = ['rectangle', 'rounded'])
    primary_color = [0.12, 0.58, 0.95, 1]
    font_color = [.3,.3,.3,1]
    border_width = 2

    def __init__(self, **kwargs):
        self.halign = 'center'
        self.valign = 'middle'
        super(FlexButtonDesktop, self).__init__(**kwargs)
        # self.text_size = self.size
        self.ripple_color = [0.0, 0.6784, 0.9569, 1]

    def on_enter(self, *args):
        self.bg_color = self.hover_color

    def on_leave(self):
        self.bg_color = self.unhover_color

Builder.load_string('''
#:import rgb kivy.utils.get_color_from_hex
#:import hex kivy.utils.get_hex_from_color

<FlexButton>:
    ripple_color: root.ripple_color
    canvas.before:
        Color:
            rgba: root.border_color
        RoundedRectangle:
            pos: root.pos
            size: root.size
            radius: root.radius
        Color:
            rgba: root.bg_color
        RoundedRectangle:
            pos: [(root.pos[0] + (root.border_weigth / 2)), (root.pos[1] + (root.border_weigth / 2))]
            size: [(root.size[0] - root.border_weigth), (root.size[1] - root.border_weigth)]
            radius: root.radius

<FlexButtonDesktop>:
    ripple_color: root.ripple_color
    # ripple_color: [0, 0, 0, .2]
    color: root.font_color
    canvas.before:
        Color:
            rgba: root.border_color
        RoundedRectangle:
            pos: root.pos
            size: root.size
            radius: root.radius
        Color:
            rgba: root.bg_color
        RoundedRectangle:
            pos: [(root.pos[0] + (root.border_weigth / 2)), (root.pos[1] + (root.border_weigth / 2))]
            size: [(root.size[0] - root.border_weigth), (root.size[1] - root.border_weigth)]
            radius: root.radius

<FlatButton>:
    color: [1,1,1,1]
    background_color: [0,0,0,0]
    shadow: True
    shadow_elevation: 2
    shadow_color: [.2,.2,.2, .3]
    bg_press: list(map(lambda c: c-.1, root.bg_normal))
    bg_normal: [.1,.5,.8,1]
    halign: 'center'
    valign: 'middle'
    markup: True
    text_hint: root.size
    background_normal: ''
    background_down: ''
    
    canvas.before:
        Color:
            rgba: root.shadow_color
        RoundedRectangle:
            pos: self.pos[0], self.pos[1] - root.shadow_elevation
            size: self.size
        Color:
            rgba: root.bg_normal if root.state == 'normal' else root.bg_press
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [5,]

<FlexImageButton>:
    icon: ''
    color: [1,1,1,1]
    background_color: [0,0,0,0]
    shadow: True
    shadow_elevation: 2
    shadow_color: [.2,.2,.2, .3]
    bg_press: list(map(lambda c: c-.1, root.bg_normal))
    bg_normal: [.1,.5,.8,1]
    halign: 'center'
    valign: 'middle'
    markup: True
    text_hint: root.size
    background_normal: ''
    background_down: ''

    canvas.before:
        Color:
            rgba: root.shadow_color
        RoundedRectangle:
            pos: self.pos[0], self.pos[1] - root.shadow_elevation
            size: self.size
        Color:
            rgba: root.bg_normal if root.state == 'normal' else root.bg_press
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [5,]
        Color:
            rgba: [1,1,1,1]
        RoundedRectangle:
            source: root.icon
            pos: self.pos[0] + 10, self.pos[1] + 10
            size: dp(24), dp(24)

<FlexIconButton>:
    # canvas.before:
    #     Color:
    #         rgba: root.border_color
    #     RoundedRectangle:
    #         pos: root.pos
    #         size: root.size
    #         radius: root.radius
    #     Color:
    #         rgba: root.bg_color
    #     RoundedRectangle:
    #         pos: [(root.pos[0] + (root.border_weigth / 2)), (root.pos[1] + (root.border_weigth / 2))]
    #         size: [(root.size[0] - root.border_weigth), (root.size[1] - root.border_weigth)]
    #         radius: root.radius

<FlexChip@Button, RippleBehavior>:
    label: 'label'
    icon: 'icon'
    size_hint: .33, .8
    background_normal: ''
    #background_pressed: ''
    font_size: '16sp'
    font_color: [.2, .2, .2, 1]
    icon_color: [1, 1, 1, 1]
    icon_size: '20sp'
    icon_size_second: '40sp'
    icon_color_second: [1, 1, 1, 1]
    font_style: 'kivy_modules//font//icons.ttf'
    markup: True
    text:  '[size=' + self.icon_size + '][color=' + hex(self.icon_color) + '][font=' + self.font_style + ']' + self.icon + '[/font][/color][/size]' + '\\n[color=' + hex(self.font_color) + ']' + self.label + '[/color]\\n[size=' + self.icon_size_second + '][sub][font=' + self.font_style + '][color=]' + hex(root.icon_color_second) + ' \uf1a5[/font]5[/sub][/size][/color]'
    background_color: [0, 0, 0, 0]
    bg_color: [255/255, 199/255, 21/255, 1]
    #color: 1,1,1,1
    #radius: 80
    text_size: self.size
    halign: 'center'
    valign: 'middle'
    canvas.before:
        Color:
            rgba: root.bg_color if root.state == 'normal' else list(map(lambda x: x - .1, root.bg_color))
        RoundedRectangle:
            pos: root.pos
            size: root.size
            #radius: [root.radius]

<FlexIconToggleButton@ToggleButton>:
    background_normal: ''
    background_color: [1,1,1,1]
    text_size: self.size
    halign: 'center'
    valign: 'middle'
    font_name: 'kivy_modules//font//icons.ttf'
    #MaterialIcons-Regular.ttf'
    font_size: '30sp'

<FlexRoundButton@Button>:
    label: ''
    icon: ''
    icon_size: '15sp'
    icon_color: [1, 1, 1, 1]
    font_size: '10sp'
    font_color: [.2, .2, .2, 1]
    markup: True
    text: ' [size=' + self.icon_size + ']' + '[color=' + hex(self.icon_color) + ']' + '[font=kivy_modules//font//icons.ttf]' + self.icon + '[/font]' + '[/color]' +  '[/size]' + '[color=' + hex(self.font_color) + ']' + self.label + '[/color]'
    background_normal: ''
    background_down: ''
    background_color: [0,0,0,0]
    bg_normal: [1, 0.78, 0.08, 1]
    bg_down: self.bg_normal[0:2] + [.5]
    color: [1,1,1,1]
    text_size: self.size
    halign: 'center'
    valign: 'middle'
    canvas.before:
        Color:
            rgba: self.bg_normal if self.state == 'normal' else self.bg_down
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [80,]

''')