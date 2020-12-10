# https://stackoverflow.com/questions/60736027/how-to-set-text-color-to-gradient-texture-in-kivy
# https://gist.github.com/tshirtman/4247921

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.properties import (
    ObjectProperty, ListProperty, NumericProperty, 
    StringProperty, OptionProperty, BooleanProperty
)

try:
    from ..behavior.hoverbehavior import HoverBehavior
    from ..behavior.buttonbehavior import ButtonBehavior
    from ..color.hex_colors import hexs
except:
    import os, sys
    from kivy.resources import resource_find
    path = os.path.dirname(os.path.dirname(resource_find(".")))
    sys.path.insert(0, path)
    from kivy_modules.behavior.buttonbehavior import ButtonBehavior
    from kivy_modules.behavior.hoverbehavior import HoverBehavior
    from kivy_modules.color.hex_colors import hexs

from itertools import chain
from random import choice, random, randint

class FlexLabelGradient(Factory.Label):
    grad = ObjectProperty(None)
    color = ListProperty([1,1,1,1])
    radius = ListProperty([10,])
    gradient = ListProperty([[]])
    gradient_orientation = OptionProperty('vertical', options = ['horizontal', 'vertical'])

    def __init__(self, **kwargs):
        super(LabelGradient, self).__init__(**kwargs)
        Clock.schedule_once(self.start)

    def start(self, evt):
        # create a 64x64 texture, defaults to rgba / ubyte
        if self.gradient_orientation == 'horizontal':
            self.grad = Texture.create(size=(len(self.gradient), 1))
        elif self.gradient_orientation == 'vertical':
            self.grad = Texture.create(size=(1, len(self.gradient)))

        buf = [str(int(v * 255)) for v in chain(*self.gradient)]
        buf = b"".join(map(lambda x: hexs[x], buf))

        # then blit the buffer
        self.grad.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.canvas.ask_update()

class FlexButtonGradient(Factory.Label, ButtonBehavior):
    background_normal = ''
    background_down = ''
    background_color = [0,0,0,0]
    grad = ObjectProperty(None)
    radius = ListProperty([10])
    color = ListProperty([1,1,1,1])
    gradient = ListProperty([[]])
    gradient_orientation = OptionProperty('vertical', options = ['horizontal', 'vertical'])

    def __init__(self, **kwargs):
        super(FlexButtonGradient, self).__init__(**kwargs)
        Clock.schedule_once(self.start)

    def start(self, evt):
        # create a 64x64 texture, defaults to rgba / ubyte
        if self.gradient_orientation == 'horizontal':
            self.grad = Texture.create(size=(len(self.gradient), 1))
        elif self.gradient_orientation == 'vertical':
            self.grad = Texture.create(size=(1, len(self.gradient)))

        self.buf_normal = [str(int(v * 255)) for v in chain(*self.gradient)]
        self.buf_normal = b"".join(map(lambda x: hexs[x], self.buf_normal))

        self.buf_down = [str(int(v * 200)) for v in chain(*self.gradient)]
        self.buf_down = b"".join(map(lambda x: hexs[x], self.buf_down))

        # then blit the buffer
        self.blitter(self.buf_normal)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.blitter(self.buf_down)
            self.dispatch('on_press')
            return True
        return super(FlexButtonGradient, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.blitter(self.buf_normal)
            self.dispatch('on_release')
            return True
        return super(FlexButtonGradient, self).on_touch_up(touch)

    def on_release(self, *args):
    	pass
 
    def on_press(self, *args):
    	pass

    # blit the buffer and update the canvas
    def blitter(self, buf):
        self.canvas.ask_update()
        self.grad.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.canvas.ask_update()

class FlexHoverGradient(HoverBehavior, Factory.Label):
    grad = ObjectProperty(None) # texture object
    radius = ListProperty([10]) # canvas curvature
    color = ListProperty([1,1,1,1]) # text color
    gradient = ListProperty([[]]) # list of lists with the colors in rgba % 100
    gradient_orientation = OptionProperty('vertical', options = ['horizontal', 'vertical'])

    def __init__(self, *args, **kwargs):
        super(HoverGradient, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.start)

    def start(self, evt):
        # change the gradient orientation
        if self.gradient_orientation == 'horizontal':
            # create the texture accordling with colors quantity
            self.grad = Texture.create(size = (len(self.gradient), 1))
        elif self.gradient_orientation == 'vertical':
            self.grad = Texture.create(size = (1, len(self.gradient)))

        # normalize the rgba to pattern 
        self.buf_normal = [str(int(v * 255)) for v in chain(*self.gradient)]
        self.buf_normal = b"".join(map(lambda x: hexs[x], self.buf_normal))

        self.buf_down = [str(int(v * 230)) for v in chain(*self.gradient)]
        self.buf_down = b"".join(map(lambda x: hexs[x], self.buf_down))

        # then blit the buffer
        self.blitter(self.buf_normal)

    def on_enter(self):
        self.blitter(self.buf_down)

    def on_leave(self):
        self.blitter(self.buf_normal)

    def blitter(self, buf):
        self.grad.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.canvas.ask_update()

class FlexRandomGradient(Factory.Label):
    grad = ObjectProperty(None)
    color = ListProperty([1,1,1,1])
    radius = ListProperty([10,])
    texture_x = NumericProperty(3)
    texture_y = NumericProperty(3)

    def __init__(self, *args, **kwargs):
        super(RandomGradient, self).__init__(*args, **kwargs)
        Clock.schedule_interval(self.random_gradient, 1)

    def random_gradient(self, evt):
        self.grad = Texture.create(size=(self.texture_x, self.texture_y), colorfmt='rgba')
        colors = list()
        for x in range(0, self.texture_x):
            for y in range(0, self.texture_y):
                colors.append([randint(0, 255), randint(0, 255), randint(0, 255), 255])

        # get all colors generated and appended in colors 
        # and transform in one list with all numbers like string
        self.buf_normal = [str(c) for c in chain(*colors)]
        # convert the buf_normal to bytes
        self.buf_normal = b"".join(map(lambda x: hexs[x], self.buf_normal))
        # blit the buffer
        self.grad.blit_buffer(self.buf_normal, colorfmt='rgba', bufferfmt='ubyte')

class FlexRadialHoverGradient(HoverBehavior, Factory.Label):
    grad = ObjectProperty(None) # texture object
    radius = ListProperty([10]) # canvas curvature
    color = ListProperty([1,1,1,1]) # text color
    radial = NumericProperty(32)
    border_color_normal = ListProperty([0, 0.7, 0.7, 1]) # get the colors in rgba%
    center_color_normal = ListProperty([1, 1, 0, 1]) # get the colors in rgba%

    def __init__(self, *args, **kwargs):
        super(RadialHoverGradient, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.start)

    def start(self, evt):
        # change the radial
        size = (self.radial, self.radial)
        self.grad = Texture.create(size = size, colorfmt = 'rgba')
        # color normalize
        self.border_color_normal = [int(v * 255) for v in self.border_color_normal]
        self.center_color_normal = [int(v * 255) for v in self.center_color_normal]
        # get the colors in down|enter depending of the behavior choosed
        self.border_color_down = [c - 10 if c >= 10 else 0 for c in self.border_color_normal]
        self.center_color_down = [c - 10 if c >= 10 else 0 for c in self.center_color_normal]
        # instacialize the buffers
        self.buf_normal = list()
        self.buf_down = list()
        # get the center of the radial
        sx_2 = size[0] // 2
        sy_2 = size[1] // 2
        
        for x in range(-sx_2, sx_2):
            for y in range(-sy_2, sy_2):
                a = x / (1.0 * sx_2)
                b = y / (1.0 * sy_2)
                d = (a ** 2 + b ** 2) ** .5

                for c in (0, 1, 2, 3):
                    self.buf_normal.append(str( max(0, min(255, int(self.center_color_normal[c] * (1 - d)) + int(self.border_color_normal[c] * d)))))
                    self.buf_down.append(str( max(0, min(255, int(self.center_color_down[c] * (1 - d)) + int(self.border_color_down[c] * d)))))
        # This assign a bytes string to the buffers 
        self.buf_normal = b"".join(map(lambda x: hexs[x], self.buf_normal))
        self.buf_down = b"".join(map(lambda x: hexs[x], self.buf_down))
        # then blit the buffer
        self.blitter(self.buf_normal)

    def on_enter(self):
        self.blitter(self.buf_down)

    def on_leave(self):
        self.blitter(self.buf_normal)

    def blitter(self, buf):
        self.grad.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.canvas.ask_update()

class FlexGradient(EventDispatcher):
    grad = ObjectProperty(None)
    color = ListProperty([1,1,1,1])
    radius = ListProperty([0,])
    gradient = ListProperty([[]])
    gradient_orientation = OptionProperty(
        'vertical', options = ['horizontal', 'vertical'])

    def __init__(self, **kwargs):
        super(Gradient, self).__init__(**kwargs)
        Clock.schedule_once(self.start)

    def start(self, evt):
        # create a 64x64 texture, defaults to rgba / ubyte
        if self.gradient_orientation == 'horizontal':
            self.grad = Texture.create(size=(len(self.gradient), 1))
        elif self.gradient_orientation == 'vertical':
            self.grad = Texture.create(size=(1, len(self.gradient)))

        buf = [str(int(v * 255)) for v in chain(*self.gradient)]
        buf = b"".join(map(lambda x: hexs[x], buf))

        # then blit the buffer
        self.grad.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.canvas.ask_update()

class FlexAnchorGradient(Factory.AnchorLayout, FlexGradient):
    pass

class FlexBoxGradient(Factory.BoxLayout, FlexGradient):
    orientation = "vertical"

Builder.load_string("""
<FlexLabelGradient>:
    canvas.before:
        # draw the gradient below the normal Label Texture
        Color:
            rgba: 1,1,1,1
        RoundedRectangle:
            texture: root.grad
            size: root.size
            pos: root.pos#int(root.center_x - root.texture_size[0] / 2.), int(root.center_y - root.texture_size[1] / 2.)
            radius: root.radius

<FlexButtonGradient>:
    text_size: self.size
    halign: 'center'
    valign: 'middle'
    canvas.before:
        # draw the gradient below the normal Label Texture
        Color:
            rgba: 1,1,1,1
        RoundedRectangle:
            texture: root.grad
            size: root.texture_size
            pos: int(root.center_x - root.texture_size[0] / 2.), int(root.center_y - root.texture_size[1] / 2.)
            radius: root.radius

<FlexHoverGradient>:
    canvas.before:
        Color:
            rgba: [1,1,1,1]
        RoundedRectangle:
            texture: root.grad
            size: root.size
            pos: root.pos
            radius: root.radius

<FlexRandomGradient>:
    canvas.before:
        Color:
            rgba: [1,1,1,1]
        RoundedRectangle:
            texture: root.grad
            size: root.size
            pos: root.pos
            radius: root.radius

<FlexRadialHoverGradient>:
    canvas.before:
        Color:
            rgba: [1,1,1,1]
        RoundedRectangle:
            texture: root.grad
            size: root.size
            pos: root.pos
            radius: root.radius

<FlexGradient>:
    canvas.before:
        Color:
            rgba: [1,1,1,1]
        RoundedRectangle:
            texture: root.grad
            size: root.size
            pos: root.pos #int(root.center_x - root.texture_size[0] / 2.), int(root.center_y - root.texture_size[1] / 2.)
            radius: root.radius

<FlexBoxGradient>:
    bg_color: [0,0,0,0]
    source: ""
    gradient: [[1,1,1,1],[.9,.9,.9,1]]
    gradient_orientation: "horizontal"

<FlexAnchorGradient>:

""")

if __name__ == '__main__':
    from kivy_modules.app import FlexApp
    from kivy.lang import Builder
    from kivy.clock import Clock
    
    class GradientApp(FlexApp):
        def get_random_colors(self):
            colors = [
                [random(),random(),random(),1],
                [random(),random(),random(),1],
                [random(),random(),random(),1]]
            return colors

        def get_orientation(self):
            return choice(['vertical', 'horizontal'])

        def build(self):
            kv = Builder.load_string('''
#:import random random.random
#:import choice random.choice

BoxLayout:
    orientation: "vertical"
    ScrollView:
        BoxLayout:
            id: container
            orientation: "vertical"
            size_hint: 1, None
            height: self.minimum_height
            padding: dp(5)
            spacing: dp(5)
            FlexLabelGradient:
                text: "Flex Gradient Label"
                size_hint: [1, None]
                height: 80
                font_size: 20
                gradient_orientation: app.get_orientation()
                gradient: app.get_random_colors()
            FlexButtonGradient:
                text: "Flex Gradient Button"
                size_hint: [1, None]
                height: 80
                font_size: 20
                gradient_orientation: app.get_orientation()
                gradient: app.get_random_colors()
            FlexHoverGradient:
                text: "Flex Hover Button"
                size_hint: [1, None]
                height: 80
                font_size: 20
                gradient_orientation: app.get_orientation()
                gradient: app.get_random_colors()
            FlexRandomGradient:
                text: "Flex Random Button"
                size_hint: [1, None]
                height: 80
                font_size: 20
            FlexBoxGradient:
                size_hint: [1, None]
                height: 160
                gradient_orientation: app.get_orientation()
                gradient: [ \
                    [0.286, 0.361, 0.827, 1.000], \
                    [0.549, 0.184, 0.678, 1.000],\
                    [0.961, 0.000, 0.451, 1.000], \
                    [1.000, 0.494, 0.024, 1.000], \
                    [1.000, 0.847, 0.463, 1.000]]
                Label:
                    text: "Flex Box Gradient"
''')

            kv.ids.container.add_widget(
                FlexRadialHoverGradient(
                    text = f"Flex Radial Hover Gradient", size_hint = [1, None],
                    border_color_normal = [0,.7,.7,1],
                    center_color_normal = [.3,.3,.3,1],
                    height = 300, font_size = 20
                ))

            return kv

    GradientApp().run()