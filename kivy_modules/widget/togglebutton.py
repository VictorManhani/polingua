from kivy.lang import Builder

from kivy.uix.togglebutton import ToggleButton

from kivy.properties import (
    ListProperty, NumericProperty, StringProperty, OptionProperty
)

from kivy.metrics import sp, dp
from kivy.uix.behaviors import TouchRippleBehavior

from ..behavior.ripplebehavior import CircularRippleBehavior, RectangularRippleBehavior
from ..behavior.hoverbehavior import HoverBehavior

class FlexToggleButton(RectangularRippleBehavior, ToggleButton, HoverBehavior):
    hover_color = ListProperty([.6,.8,1,1])
    unhover_color = ListProperty([1,1,1,1])
    ripple_duration_in_fast = 0.2
    background_color = [0,0,0,0]
    background_normal = ''
    background_down = ''
    color = ListProperty([0.0, 0.4471, 0.8235, 1])
    radius = [10,]
    bg_color = ListProperty([1,1,1,1])
    border_color = ListProperty([0.0, 0.4471, 0.8235, 1])
    border_weigth = NumericProperty(dp(1))

    primary_color = [0.12, 0.58, 0.95, 1]
    font_size = NumericProperty(sp(20))
    font_color = ListProperty([.3,.3,.3,1])
    border_width = 2

    def __init__(self, **kwargs):
        super(FlexToggleButton, self).__init__(**kwargs)
        self.halign = 'center'
        self.valign = 'middle'
        self.ripple_color = [0.0, 0.6784, 0.9569, 1]

    # def on_enter(self, *args):
    #     self.bg_color = self.hover_color

    # def on_leave(self):
    #     self.bg_color = self.unhover_color

    def on_state(self, obj, state):
        self.bg_color = self.hover_color if state == "down" else self.unhover_color

Builder.load_string('''
#:import rgb kivy.utils.get_color_from_hex
#:import hex kivy.utils.get_hex_from_color
#:import icons kivy_modules.icons.md_icons

<FlexToggleButton>:
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
''')