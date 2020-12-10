from typing import List
from kivy.lang import Builder
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.properties import (
    ListProperty, NumericProperty, StringProperty, 
    BooleanProperty, ObjectProperty, OptionProperty
)
from ..behavior.ripplebehavior import CircularRippleBehavior, RectangularRippleBehavior
from kivy.metrics import sp, dp

from ..behavior.hoverbehavior import HoverBehavior

class FlexSpinner(RectangularRippleBehavior, Spinner, HoverBehavior):
    background_color = [0,0,0,0]
    background_normal = ''
    background_down = ''
    ripple_duration_in_fast = 0.2

    color = ListProperty([0.0, 0.4471, 0.8235, 1])
    fg_color = ListProperty([.3,.3,.3,1])
    ripple_color = ListProperty([0.0, 0.6784, 0.9569, 1])
    border_color = ListProperty([0.0, 0.4471, 0.8235, 1])
    primary_color = [0.12, 0.58, 0.95, 1]
    hover_color = ListProperty([.6,.8,1,1])
    unhover_color = ListProperty([1,1,1,1])
    bg_color = ListProperty([1,1,1,1])
    bg_color_normal = ListProperty([1,1,1,1])
    bg_color_press = ListProperty([.9,.9,.9,1])

    font_size = sp(20)
    radius = ListProperty([10,])
    border_weigth = NumericProperty(dp(1))
    font_size = NumericProperty(20)
    border_width = 2
    dropdown_max_height = NumericProperty(50)

    def __init__(self, **kwargs):
        super(FlexSpinner, self).__init__(**kwargs)
        self.halign = 'center'
        self.valign = 'middle'
        self.ripple_color = kwargs.get("ripple_color", self.ripple_color)
        self.fg_color = kwargs.get("fg_color", self.fg_color)
        self.bg_color = kwargs.get("bg_color", self.bg_color)

    def on_dropdown_font_size(self, obj, number):
        self.option_cls.font_size = number

    def on_dropdown_max_height(self, obj, number):
        self.dropdown_cls.max_height = number

    def on_fg_color(self, obj, val):
        self.color = val

    def on_press(self, *args):
        self.bg_color = self.bg_color_press

    def on_release(self, *args):
        self.bg_color = self.bg_color_normal

    # def on_enter(self, *args):
    #     self.bg_color = self.hover_color

    # def on_leave(self):
    #     self.bg_color = self.unhover_color

class FlexSpinnerOption(SpinnerOption, HoverBehavior):
    background_color = ListProperty([.8, .8, .8, 1])
    hover_color = ListProperty([.5, .5, 1, 1])
    unhover_color = ListProperty([.8, .8, .8, 1])
    font_size = NumericProperty(12)
    
    def on_enter(self):
        self.background_color = self.hover_color
    
    def on_leave(self):
        self.background_color = self.unhover_color

class IconSpinner(Spinner, HoverBehavior):
    icon = StringProperty('')
    background_color = ListProperty([.5, .5, .5, 1])
    hover_color = ListProperty([.5, .5, 1, 1])
    unhover_color = ListProperty([.5, .5, .5, 1])
    
    def on_enter(self):
        self.background_color = self.hover_color
    
    def on_leave(self):
        self.background_color = self.unhover_color
    
class IconSpinnerOption(SpinnerOption, HoverBehavior):
    background_color = ListProperty([.8, .8, .8, 1])
    hover_color = ListProperty([.5, .5, 1, 1])
    unhover_color = ListProperty([.8, .8, .8, 1])
    
    def on_enter(self):
        self.background_color = self.hover_color
    
    def on_leave(self):
        self.background_color = self.unhover_color

Builder.load_string('''
#:import rgb kivy.utils.get_color_from_hex
#:import hex kivy.utils.get_hex_from_color
#:import icons kivy_modules.icons.md_icons

<FlexSpinnerOption>:
    markup: True
    background_normal: ''
    color: [.2, .2, .2, 1]
    background_color: [.8, .8, .8, 1]

<FlexSpinner>:
	markup: True
	text: ''
	background_normal: ''
    color: [.2, .2, .2, 1]
	text_size: self.size
	halign: 'center'
	valign: 'middle'
    option_cls: "FlexSpinnerOption"
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

<IconSpinnerOption>:
    markup: True
    background_normal: ''
    color: [.2, .2, .2, 1]
    background_color: [.8, .8, .8, 1]
    
<IconSpinner>:
    label: ''
	icon: 'language-python'
	font_size: '20sp'
	markup: True
	text: '[font=kivy_modules\\\\font\\\\icons.ttf]' + icons[self.icon] + '[/font]' + ' [size=' + str(int(self.font_size)) + ']' + self.label + '[/size]'
	background_normal: ''
    color: [.2, .2, .2, 1]
	text_size: self.size
	halign: 'center'
	valign: 'middle'
    background_normal: ''
    option_cls: "IconSpinnerOption"
''')
