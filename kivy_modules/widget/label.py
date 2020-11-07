from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.metrics import sp, dp

from kivy.clock import Clock
from kivy.properties import (
    StringProperty, ObjectProperty, BooleanProperty,
    NumericProperty, ListProperty
)
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

import json
import pprint

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
		

class FlexLabel(Label):
	font_size = NumericProperty(sp(20))
	fg_color = ListProperty([.1,.1,.1,1])
	bold = BooleanProperty(False)
	radius = ListProperty([0])
	color = fg_color

	def on_fg_color(self, obj, val):
		self.color = val

# label with a pretty representation of text
# inspired by pprint module
class PrettyLabel(ScrollView):
    text = StringProperty('')
    padding = 10
    radius = ListProperty([0])

    def init(self, *args, **kwargs):
        super(PrettyLabel, self).init(*args, **kwargs)
        self.text = '%s' % 'hello top day dia africanner ' * 100

    def pprint(self, obj, sort_keys = False, indent = 4):
        """Pretty-print a Python object to a stream [default is sys.stdout]."""
        # pprint.pprint(
        #     obj, indent = indent, width = self.width,
        #     depth = 1, stream = self,
        # )

        self.text = json.dumps(
            obj, sort_keys = sort_keys,
            indent = indent, separators = (',', ': ')
		)

    def write(self, text):
        self.text += text

Builder.load_string('''
<PrettyLabel>:
	do_scroll_y: True
	do_scroll_x: True
    scroll_type: ['bars']
    bar_width: dp(10)
    bar_color: [.2, .2, 1, 1]
    effect_cls: 'ScrollEffect'
    Label:
		# color: [.2,.2, .2, 1]
        size_hint: None, None
        width: dp(600)
        height: self.texture_size[1]
        text_size_x: self.width
        padding: 10, 10
        text: root.text
        # markup: True
        # # text_size: self.size
        # halign: 'left'
        # valign: 'middle'
        # padding: 10, 10
        canvas.before:
			Color:
				rgba: [.3,.3,.3,1]
			Rectangle:
				pos: self.pos
				size: self.size

<ScrollableLabel>:
	Label:
		size_hint_y: None
		height: self.texture_size[1]
		text_size: self.width, None
		text: root.text
		markup: True

<FlexLabel>:
	color: [.1,.1,.1,1]
	bg_color: [1, 1, 1, 0]
	text_size: self.size
	halign: 'center'
	valign: 'middle'
	radius: [0,]
	canvas.before:
		Color:
			rgba: root.bg_color
		RoundedRectangle:
			pos: root.pos
			size: root.size
			radius: root.radius
''')




