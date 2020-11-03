from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.core.window import Window
# Window.size = [500, 500]
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.properties import StringProperty, ObjectProperty, \
    ListProperty, AliasProperty, BooleanProperty, NumericProperty

from PIL import Image as PILImage
import imageio
import functools
import cv2
import os

from kivy.graphics import *
from kivy.graphics.svg import Svg
from kivy.graphics import Scale

class FlexSvg(Widget):
    source = StringProperty("nave-espacial.svg")
    bg_color = ListProperty([1,1,1,1])
    radius = ListProperty([10])

    def __init__(self, **kwargs):
        super(FlexSvg, self).__init__(**kwargs)
        Clock.schedule_once(self.start)

    def start(self, evt):
        with self.canvas.before:
            self.gradients = [[1,0,0,1], [0,0,1,1]]
            self.color = Color(1,0,0,1)
            self.scale = Scale(1, 1, 1)
            self.svg = Svg(self.source)

        self.bind(size=self._do_scale)
        self.size = self.svg.width, self.svg.height
 
    def _do_scale(self, *args):
        self.scale.xyz = (
            self.width / self.svg.width,
            self.height / self.svg.height,
            1
        )

Builder.load_string("""
<FlexSvg>:
    # canvas.before:
    #     Color:
    #         rgba: root.bg_color
    #     RoundedRectangle:
	# 		pos: root.pos
    #         size: root.size
    #         radius: root.radius
""")

# if __name__ == '__main__':
class Home(Factory.BoxLayout):
    orientation = "vertical"

    def __init__(self, *args, **kwargs):
        super(Home, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.start, 0)

    def start(self, evt):
        pass

class SvgApp(App):
    title = "Svg"

    def build(self):
        return Builder.load_string("""
Home:
    Button:
        text: "Hello World"
    FlexSvg:
        source: "esportes-e-competicao.svg"
""")

SvgApp().run()