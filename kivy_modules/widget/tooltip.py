from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import StringProperty

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_string("""
<Tooltip>:
	size_hint: None, None
	size: self.texture_size[0]+5, self.texture_size[1]+5
	canvas.before:
		Color:
			rgba: .96, .96, 0.59, 1
		Rectangle:
			size: self.size
			pos: self.pos

<Home>:
	BoxLayout:
		orientation: 'vertical'
		MyButton:
			text: 'text1'
		MyButton:
			text: 'text2'
""")

class Tooltip(Label):
	text = StringProperty("")
	color = [.2, .2, .2, 1]

class MyButton(Button):
	tooltip = Tooltip()

	def __init__(self, **kwargs):
		Window.bind(mouse_pos = self.on_mouse_pos)
		super(Button, self).__init__(**kwargs)

	def on_mouse_pos(self, *args):
		if not self.get_root_window(): return
		pos = args[1]
		if (pos[0] + self.tooltip.size[0]) > Window.width:
			pos = [pos[0] - self.tooltip.size[0], pos[1]]
		if (pos[1] + self.tooltip.size[1]) > Window.height:
			pos = [pos[0], pos[1] - self.tooltip.size[1]]

		self.tooltip.pos = pos
		Clock.unschedule(self.display_tooltip) # cancel scheduled event since I moved the cursor
		self.close_tooltip() # close if it's opened
		if self.collide_point(*self.to_widget(*pos)):
			self.tooltip.text = self.text
			Clock.schedule_once(self.display_tooltip, .1)

	def on_release(self, *args):
		print(self.text)

	def on_touch_down(self, *args):
		super(Button, self).on_touch_down(*args)
		self.close_tooltip()

	def close_tooltip(self, *args):
		Window.remove_widget(self.tooltip)

	def display_tooltip(self, *args):
		Window.add_widget(self.tooltip)

if __name__ == '__main__':
	class Home(Screen):
		pass

	class ClientApp(App):
		def build(self):
			return Home()

	ClientApp().run()
