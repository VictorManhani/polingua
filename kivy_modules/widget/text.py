from kivy.lang import Builder
from kivy.clock import Clock

from kivy.uix.textinput import TextInput
from kivy.properties import (
    StringProperty, ListProperty, NumericProperty, 
	BooleanProperty, ObjectProperty)
from kivy.metrics import sp, dp

from kivy.core.window import Window
from kivy.utils import get_hex_from_color
from ..icons import md_icons

from kivy.uix.textinput import TextInput

from pprint import PrettyPrinter

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
	def __init__(self, **kwargs):
		self.background_color = [0,0,0,0]
		self.background_normal = ''
		self.background_active = ''
		#self.color = [1,0,0,1] #[0.0, 0.4471, 0.8235, 1]
		self.font_size = sp(20)
		self.radius = [10,]
		self.border_weigth = dp(1)
		self.bg_color = [0, 0, 1, 1]
		self.border_color = [0.0, 0.4471, 0.8235, 1]
		self.cursor_color = [0, 0, 1, 1]
		self.halign = 'center'
		self.valign = 'middle'
		self.hint_text_color = [0.0, 0.4471, 0.8235, .5]
		self.foreground_color = [0.0, 0.4471, 0.8235, 1]
		self.background_color = [0,0,0,0]
		super().__init__(**kwargs)

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

class FlexPrettyText(FlexText):
    pp = ObjectProperty(None)
    data = ListProperty()
    wid = NumericProperty(100)
    depth = NumericProperty(None)
    indent = NumericProperty(2)
    compat = BooleanProperty(False)
    sort_dicts = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.indent = kwargs.get("indent", self.indent)
        self.wid = kwargs.get("wid", self.wid)
        self.depth = kwargs.get("depth", self.depth)
        self.data = kwargs.get("data", self.data)
        self.compat = kwargs.get("compat", self.compat)
        self.sort_dicts = kwargs.get("sort_dicts", self.sort_dicts)

        self.pp = PrettyPrinter(
            stream=self, indent=self.indent, 
            width=self.wid, depth=self.depth, 
            compact=self.compat, sort_dicts=self.sort_dicts)

    def write(self, *args):
        self.text += args[0]

    def ppri(self):
        if self.pp:
            self.pp.pprint(self.data)

    def on_pp(self, obj, val):
        self.ppri()

    def on_data(self, obj, val):
        self.ppri()

    def on_indent(self, obj, val):
        self.ppri()

    def on_wid(self, obj, val):
        self.ppri()

    def on_depth(self, obj, val):
        self.ppri()

    def on_compat(self, obj, val):
        self.ppri()

    def on_sort_dicts(self, obj, val):
        self.ppri()

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
    halign: "left"
    valign: "middle"

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
''')



