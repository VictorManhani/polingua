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
    hover_color = ListProperty([.6,.8,1,1])
    unhover_color = ListProperty([1,1,1,1])
    ripple_duration_in_fast = 0.2
    background_color = [0,0,0,0]
    background_normal = ''
    background_down = ''
    color = ListProperty([0.0, 0.4471, 0.8235, 1])
    font_size = sp(20)
    radius = [10,]
    bg_color = ListProperty([1,1,1,1])
    border_color = ListProperty([0.0, 0.4471, 0.8235, 1])
    border_weigth = NumericProperty(dp(1))
    primary_color = [0.12, 0.58, 0.95, 1]
    font_color = [.3,.3,.3,1]
    font_size = NumericProperty(20)
    border_width = 2
    dropdown_max_height = NumericProperty(50)

    def __init__(self, **kwargs):
        super(FlexSpinner, self).__init__(**kwargs)
        self.halign = 'center'
        self.valign = 'middle'
        self.ripple_color = kwargs.get("ripple_color", [0.0, 0.6784, 0.9569, 1])

    def on_dropdown_font_size(self, obj, number):
        self.option_cls.font_size = number

    def on_dropdown_max_height(self, obj, number):
        self.dropdown_cls.max_height = number

    def on_enter(self, *args):
        self.bg_color = self.hover_color

    def on_leave(self):
        self.bg_color = self.unhover_color

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
