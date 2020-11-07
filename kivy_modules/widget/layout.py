from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import (
	ListProperty, BooleanProperty, ObjectProperty, StringProperty
)

class FlexLayout(BoxLayout):
	bg_color = ListProperty([1,1,1,1])
	source = StringProperty("")
	radius = ListProperty([0])

class NewBoxLayout(BoxLayout):
	radius = ListProperty([0])

class SmartLayout(BoxLayout):
	background_color = ListProperty([0,0,0,1]) # [.8,.8,.8,1]
	radius = ListProperty([0])

class SmartIcon(Widget):
	text = StringProperty('')
	move = False
	selected = False
	radius = ListProperty([0])

	def __init__(self, *args, **kwargs):
		super().__init__()
		self.bind(on_touch_down = self.on_press)
		self.bind(on_touch_up = self.on_release)
		self.bind(on_touch_move = self.on_move)
		Window.bind(mouse_pos = self.on_touch)

	def on_press(self, instance, touch):
		if self.collide_point(*touch.pos):
			self.selected = True
			# ~ self.pos = Window.mouse_pos[0] - self.size[0] / 2, Window.mouse_pos[1] - self.size[1] / 2
			 
	def on_release(self, instance, touch):
		if self.collide_point(*touch.pos):
			pass
			# ~ self.pos = Window.mouse_pos[0] - self.size[0] / 2, Window.mouse_pos[1] - self.size[1] / 2
	
	def on_move(self, instance, touch):
		if self.collide_point(*touch.pos) and self.move:
			#self.pos = Window.mouse_pos[0] - self.size[0] / 2, Window.mouse_pos[1] - self.size[1] / 2
			self.pos = touch.pos[0] - self.size[0] / 2, touch.pos[1] - self.size[1] / 2

	def on_touch(self, *args):
		#if not self.get_root_window(): return
		pos = args[1]
		if self.collide_point(*pos) and self.selected == False:
			self.hover_color = [1,1,1,.05]
		elif self.collide_point(*pos) and self.selected:
			self.hover_color = [1,1,1,.25]
		elif not self.collide_point(*pos) and self.selected:
			self.hover_color = [1,1,1,.2]
		elif not self.collide_point(*pos) and not self.selected:
			self.hover_color = [0,0,0,0]

Builder.load_string('''
<FlexLayout>:
	orientation: 'vertical'
	radius: [0,]
	padding: dp(5)
	spacing: dp(5)
	canvas.before:
		Color:
			rgba: root.bg_color
		RoundedRectangle:
			pos: root.pos
			size: root.size
			radius: root.radius
			source: root.source

<NewBoxLayout>:
	orientation: 'vertical'
	background_color: [1,1,1,1]
	radius: [0,]
	source: ''
	canvas.before:
		Color:
			rgba: root.background_color
		RoundedRectangle:
			pos: root.pos
			size: root.size
			source: root.source
			radius: root.radius

<SmartLayout>:
	source: ''
	radius: [0,]
	background_color: [0,0,0,1]
	canvas.before:
		Color:
			rgba: root.background_color
		RoundedRectangle:
			pos: root.pos
			size: root.size
			source: root.source
			radius: root.radius

<SmartIcon>:
	background_color: [1,1,1,1]
	hover_color: [0,0,0,0]
	radius: [0,]
	source: ''
	text: ''
	size_hint: None, None
	size: dp(50), dp(50)
	canvas.before:
		Color:
			rgba: root.hover_color
		Rectangle:
			pos: root.pos[0], root.pos[1]
			size: root.size[0], root.size[1]
		Color:
			rgba: root.background_color
		RoundedRectangle:
			pos: root.pos[0], root.pos[1]
			size: root.size[0], root.size[1]
			source: root.source
			radius: root.radius

<FloatLayout>:
	orientation: 'vertical'
	background_color: [1,1,1,1]
	radius: [0,]
	source: ''
	canvas.before:
		Color:
			rgba: root.background_color
		RoundedRectangle:
			pos: root.pos
			size: root.size
			source: root.source
			radius: root.radius

# <BoxLayout>:
# 	background_color: [1,1,1,1]
# 	radius: [0,]
# 	source: ''
# 	canvas.before:
# 		Color:
# 			rgba: root.background_color
# 		RoundedRectangle:
# 			pos: root.pos
# 			size: root.size
# 			source: root.source
# 			radius: root.radius
''')
