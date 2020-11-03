from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import (
	StringProperty, ListProperty, ObjectProperty
)

class FlexWidget(Widget):
	bg_color = ListProperty([0,0,0,0])
	fg_color = ListProperty([.1,.1,.1,1])
	radius = ListProperty([0])
	source = StringProperty()
	texture = ObjectProperty()

Builder.load_string('''
<FlexWidget>:
	canvas.before:
		Color:
			rgba: root.bg_color
		RoundedRectangle:
			pos: root.pos
			size: root.size
			radius: root.radius
			source: root.source
			texture: root.texture
''')





