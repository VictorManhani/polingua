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
from kivy.graphics.texture import Texture
import functools
import cv2
import os

class FlexGif(Widget):
    source = StringProperty("kivy_modules/asset/loader.gif")
    anim_delay = NumericProperty(0.1)
    background_color = ListProperty([1,1,1,1])
    radius = ListProperty([10])
    _loop_evt = ObjectProperty(None, allownone=True)
    _texture = ObjectProperty(None, allownone=True)
    _gif_frames = ObjectProperty(None, allownone=True)
    _number_of_frames = NumericProperty(0)
    _current_frame = NumericProperty(0)
    loop = True

    def __init__(self, **kwargs):
        super(FlexGif, self).__init__(**kwargs)
        Clock.schedule_once(self.start)

    def start(self, evt):
        Clock.schedule_once(self.get_gif)

    def on_source(self, obj, val):
        Clock.schedule_once(self.get_gif)

    def get_gif(self, evt):
        if not self.source:
            return

        self.load_image(self.source)
        Clock.schedule_once(self.show_gif)
        self.start_gif()

    def load_image(self, file_path):
        old_file_path = file_path
        file_path = resource_find(old_file_path)
        if not file_path:
            file_path = os.path.abspath(old_file_path)

        filename, file_extension = os.path.splitext(file_path)
        file_extension = file_extension[1:].lower()
        self._gif_frames = list()

        # open a image resized with the window size
        if file_extension in ['png', 'jpg', 'jpeg']:
            self._number_of_frames = 1
            self.gif_np = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            self.gif_np = cv2.cvtColor(self.gif_np, cv2.COLOR_BGRA2RGBA)
            self.gif_np = cv2.resize(self.gif_np, Window.size)
            size = self.gif_np.shape[0:2]
            data = self.gif_np.tostring()
            texture = Texture.create(size=size, colorfmt="rgba")
            texture.blit_buffer(data, bufferfmt="ubyte", colorfmt="rgba")
            self._gif_frames.append(texture)
        # open a gif to manipulate
        elif file_extension in 'gif':
            self.gif_np = imageio.get_reader(file_path)
            self._number_of_frames = len(self.gif_np)
            for frame in self.gif_np:
                # each frame is a numpy matrix
                size = frame.shape[0:2]
                texture = Texture.create(size=size, colorfmt="rgba")
                data = frame.tostring()
                texture.blit_buffer(data, bufferfmt="ubyte", colorfmt="rgba")
                self._gif_frames.append(texture)

    def show_gif(self, evt):
        self._texture = self._gif_frames[0]

    def start_gif(self):
        def looping_gif(evt):
            self._current_frame += 1
            if self._current_frame >= self._number_of_frames:
                self._current_frame = 0
            if self.loop == False:
                Clock.unschedule(self._loop_evt)
            self._texture = self._gif_frames[self._current_frame]
        self._loop_evt = Clock.schedule_interval(looping_gif, self.anim_delay)

    def set_frame_by_index(self, index):
        try:
            self._texture = self._gif_frames[int(index)]
        except:
            pass

Builder.load_string("""
<FlexGif>:
    canvas.before:
        Color:
            rgba: root.background_color
        RoundedRectangle:
            texture: root._texture
			pos: [root.x, root.y + (root.height - root.width) / 2]
            size: (root.width, root.width) if root.height > root.width else (root.height, root.height) 
            radius: root.radius
""")

if __name__ == '__main__':
    class MyGifVideo(Factory.ButtonBehavior, Gif):
        pass

    class Home(Factory.BoxLayout):
        orientation = "vertical"
        
        def __init__(self, *args, **kwargs):
            super(Home, self).__init__(*args, **kwargs)
            Clock.schedule_once(self.start, 3)

        def start(self, evt):
            self.myimage = self.ids.myimage
            self.slider = self.ids.slider

            self.slider.min = 0
            self.slider.max = self.myimage._number_of_frames
            
            self.slider.bind(value = self.on_change)
            
        def on_change(self, instance, value):
            self.myimage.set_frame_by_index(value)

    class GifApp(App):
        title = "Gif"
        def build(self):
            return Builder.load_string("""
    Home:
        MyGifVideo:
            id: myimage
            # source: "test1.jpg"
            source: "test.gif"
            size_hint: [1, .9]
            on_release:
                self.start_gif()
        Slider:
            id: slider
            size_hint: [1, .1]
            value_track: True
            value_track_color: [1, 0, 0, 1]
            step: 1
    """)

    GifApp().run()