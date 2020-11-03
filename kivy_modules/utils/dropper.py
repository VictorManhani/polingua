# https://stackoverflow.com/questions/38337947/highlight-a-kivy-togglebutton-with-mouse-hovering
# https://kivy.org/doc/stable/api-kivy.core.window.html
# https://stackoverflow.com/questions/42877426/is-it-possible-to-make-a-button-transparent-kivy
# https://coredump.pt/questions/14014955/kivy-how-to-change-window-size
# https://stackoverflow.com/questions/45199329/python-kivy-float-layout
# https://kivy.org/doc/stable/installation/installation-windows.html
# https://www.reddit.com/r/kivy/comments/6a5grq/how_to_use_scrollview/
# https://stackoverflow.com/questions/18215388/kivy-horizontal-listview
# https://coredump.pt/questions/19005182/rounding-button-corners-in-kivy
# https://stackoverflow.com/questions/50570040/conditional-expression-in-kivy-lang
# https://unixuniverse.com.br/linux/automacao-pyautogui
# https://stackoverflow.com/questions/44630915/kivy-reference-text-of-textinput-by-stringproperty?rq=1
# https://stackoverflow.com/questions/17392202/passing-image-object-as-a-button-background-in-kivy
# https://stackoverflow.com/questions/42099231/how-to-change-background-colour-in-kivy?rq=1
# https://pt.stackoverflow.com/questions/143552/entendendo-o-conceito-de-threads-na-pr%C3%A1tica-em-python
# https://www.youtube.com/watch?v=kJshtCfqCsY
# https://stackoverflow.com/questions/42099231/how-to-change-background-colour-in-kivy?rq=1
# https://groups.google.com/forum/#!topic/kivy-users/OmV9O-suwrM

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty
from kivy.core.window import Window
from kivy.utils import get_hex_from_color

import pynput.mouse
import pyautogui

kv = Builder.load_string('''
#:import Clipboard kivy.core.clipboard.Clipboard

<Texto@TextInput>:
    font_size: tam_font
    #padding_x: [30,30]
    padding_y: 20
    #background_color: 1,1,1,1
    background_color: 1,1,1,0
    cursor_color: 1,1,1,1
    hint_text: 'Body'
    text_align: 'center'
	text_valign: 'center'
    canvas.before:
        Color:
            rgba: 1,1,1,1
    canvas.after:
        Color:
			rgb: 0,0,0,1
		Line:
			points: self.pos[0] , self.pos[1], self.pos[0] + self.size[0], self.pos[1] 

<FlatLabel@Label>:
	text_size: self.size
	font_size: sp(17)
	size_hint_x: .2
	outline_color: [0,0,0,1]
	outline_width: 1
	halign: "center"
	valign: "middle"

<FlatButton@Button>:
	size_hint_x: .8
	on_release:
		Clipboard.copy(self.text)

<Home>:
	orientation: 'vertical'
	padding: 10
	spacing: 10
	canvas.before:
		Color:
			rgba: root.bg_color
		Rectangle:
			size: self.size
			pos: self.pos
	BoxLayout:
		FlatLabel:
			text: "rgb%"
		FlatButton:
			id: rgb%
	BoxLayout:
		FlatLabel:
			text: "rgba"
		FlatButton:
			id: rgba
	BoxLayout:
		FlatLabel:
			text: "hex"
		FlatButton:
			id: hex
	BoxLayout:
		FlatLabel:
			text: "hsb"
		FlatButton:
			id: hsb
''')

class Home(BoxLayout):
	bg_color = ListProperty([1,1,1,1])
	is_app_window = False

	def __init__(self, **kwargs):
		super(Home, self).__init__(**kwargs)
		self.mouse_listener()
		Window.bind(on_cursor_enter=self.mouse_enter)
		Window.bind(on_cursor_leave=self.mouse_leave)

	def mouse_enter(self, instance):
		self.is_app_window = True

	def mouse_leave(self, instance):
		self.is_app_window = False

	def mouse_listener(self):
     	# GERA UM ESCUTADOR DA FUNCAO ON_CLICK
		listener = pynput.mouse.Listener(
			on_click=self.on_click)
		listener.start()

	def on_click(self, x, y, click_button, click_bool):
     	# A cada click eu capturo a cor que o mouse está apontando.
		if click_bool and not self.is_app_window:
			c = pyautogui.pixel(x, y)
			color = [c[0]/255, c[1]/255, c[2]/255, 1]
			self.bg_color = color
			hex_color = get_hex_from_color(color)

			cc = list(c[:])
			cc.append(255)
			hsv = self.rgb_2_hsv(cc)

			color_texto = f'[{color[0]:.3f}, {color[1]:.3f}, {color[2]:.3f}, {color[3]:.3f}]'

			self.ids['rgb%'].text = color_texto
			self.ids['rgba'].text = f"[{c[0]}, {c[1]}, {c[2]}, 255]"
			self.ids['hex'].text = f"{hex_color}"
			self.ids['hsb'].text = f"[{hsv[0]},{hsv[1]},{hsv[2]}]"

			return True

	def rgb_2_hsv(self, rgba):
		''' Converts an integer RGB tuple (value range from 0 to 255) to an HSV tuple '''
		# Unpack the tuple for readability
		R, G, B, A = rgba
		# Compute the H value by finding the maximum of the RGB values
		RGB_Max, RGB_Min = max(rgba[0:3]), min(rgba[0:3])
		# Compute the value
		V = RGB_Max
		if V == 0: H = S = 0; return (H,S,V);
		# Compute the saturation value
		S = 255 * (RGB_Max - RGB_Min) // V
		if S == 0: H = 0; return (H, S, V);
		# Compute the Hue
		if RGB_Max == R: H = 0 + 43*(G - B)//(RGB_Max - RGB_Min)
		elif RGB_Max == G: H = 85 + 43*(B - R)//(RGB_Max - RGB_Min)
		else: H = 171 + 43*(R - G)//(RGB_Max - RGB_Min)
		return (H, S, V)

class DropperApp(App):
	title = 'Dropper 3'

	def build(self):
		return Home()

if __name__ == "__main__":
	DropperApp().run()
