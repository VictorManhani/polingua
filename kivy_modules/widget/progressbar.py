from typing import List
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
from kivy.lang.builder import Builder
from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangle
from kivy.clock import Clock
from kivy.properties import (
    NumericProperty, AliasProperty, ListProperty,
    OptionProperty, BooleanProperty, BoundedNumericProperty, 
    ReferenceListProperty, ObjectProperty)

import random

class CircularProgressBar(ProgressBar):
    thickness = NumericProperty(40)
    label = ObjectProperty(None)
    texture_size = ObjectProperty(None)
    max = NumericProperty(100)
    min = NumericProperty(0)
    value = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set constant for the bar thickness
        self.thickness = kwargs.get("thickness", self.thickness)

        # Create a direct text representation
        self.label = CoreLabel(text="0%", font_size=self.thickness)

        # Initialise the texture_size variable
        self.texture_size = kwargs.get("texture_size", self.texture_size)

        # GET VALUES NEW OR DEFAULT
        self.max = kwargs.get("max", self.max)
        self.min = kwargs.get("min", self.min)
        self.value = kwargs.get("value", self.value)

        # Refresh the text
        self.refresh_text()

        # Redraw on innit
        self.draw()

    def draw(self):

        with self.canvas:
            
            # Empty canvas instructions
            self.canvas.clear()

            # Draw no-progress circle
            Color(0.26, 0.26, 0.26)
            Ellipse(pos=self.pos, size=self.size)

            # Draw progress circle, small hack if there is no progress (angle_end = 0 results in full progress)
            Color(random.random(), 0, 0)
            Ellipse(pos=self.pos, size=self.size,
                    angle_end=(0.001 if self.value_normalized == 0 else self.value_normalized*360))

            # Draw the inner circle (colour should be equal to the background)
            Color(0, 0, 0)
            Ellipse(pos=(self.pos[0] + self.thickness / 2, self.pos[1] + self.thickness / 2),
                    size=(self.size[0] - self.thickness, self.size[1] - self.thickness))

            # Center and draw the progress text
            Color(1, 1, 1, 1)
            #added pos[0]and pos[1] for centralizing label text whenever pos_hint is set
            Rectangle(texture=self.label.texture, size=self.texture_size,
                  pos=(self.size[0] / 2 - self.texture_size[0] / 2 + self.pos[0], self.size[1] / 2 - self.texture_size[1] / 2 + self.pos[1]))

    def refresh_text(self):
        # Render the label
        self.label.refresh()

        # Set the texture size each refresh
        self.texture_size = list(self.label.texture.size)

    def set_value(self, value):
        # Update the progress bar value
        self.value = value

        # Update textual value and refresh the texture
        self.label.text = str(int(self.value_normalized*100)) + "%"
        self.refresh_text()

        # Draw all the elements
        self.draw()

class TrackLoadProgressBar(Widget):
    min = NumericProperty(0.)
    max = NumericProperty(100.)
    range = ReferenceListProperty(min, max)
    step = BoundedNumericProperty(0, min=0)

    radius = ListProperty([5])
    orientation = OptionProperty('horizontal', options=('vertical', 'horizontal'))
    padding = NumericProperty('16sp') # default: 16sp

    value_track_width = NumericProperty('10dp')

    value_track = BooleanProperty(True)
    value_track_color = ListProperty([1, 0, 0, 1])
    value_pos = ListProperty([100,100])

    loading_value_track = BooleanProperty(True)
    loading_value_track_color = ListProperty([.518, .518, .518, 1])
    loading_value_pos = ListProperty([100,100])

    _value = 0.
    _loading_value = 0.
    
    border_horizontal = ListProperty([0, 18, 0, 18])
    border_vertical = ListProperty([18, 0, 18, 0])

    sensitivity = OptionProperty('all', options=('all', 'handle'))
    cursor_width = NumericProperty('24sp')
    cursor_height = NumericProperty('24sp')
    cursor_size = ReferenceListProperty(cursor_width, cursor_height)
    cursor_radius = ListProperty([50])
    cursor_color = ListProperty([1,0,0,1])

    bar_color = ListProperty([1,1,1,1])

    def __init__(self, **kwargs):
        super(TrackLoadProgressBar, self).__init__(**kwargs)

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        value = max(0, min(self.max, value))
        if value != self._value:
            self._value = value
            return True

    value = AliasProperty(_get_value, _set_value)

    def _get_loading_value(self):
        return self._loading_value

    def _set_loading_value(self, loading_value):
        loading_value = max(0, min(self.max, loading_value))
        if loading_value != self._loading_value:
            self._loading_value = loading_value
            return True
        
    loading_value = AliasProperty(_get_loading_value, _set_loading_value)
    
    def get_norm_value(self):
        d = self.max
        if d == 0:
            return 0
        return self.value / float(d)

    def set_norm_value(self, value):
        self.value = value * self.max

    value_normalized = AliasProperty(get_norm_value, set_norm_value, bind=('value', 'max'), cache=True)

    def get_loading_norm_value(self):
        d = self.max
        if d == 0:
            return 0
        return self.loading_value / float(d)

    def set_loading_norm_value(self, loading_value):
        self.loading_value = loading_value * self.max

    loading_value_normalized = AliasProperty(get_loading_norm_value, set_loading_norm_value, bind=('loading_value', 'max'), cache=True)

    def get_value_pos(self):
        padding = self.padding
        x = self.x
        y = self.y
        nval = self.value_normalized
        if self.orientation == 'horizontal':
            return (x + padding + nval * (self.width - 2 * padding), y)
        else:
            return (x, y + padding + nval * (self.height - 2 * padding))

    def set_value_pos(self, pos):
        padding = self.padding
        x = min(self.right - padding, max(pos[0], self.x + padding))
        y = min(self.top - padding, max(pos[1], self.y + padding))
        if self.orientation == 'horizontal':
            if self.width == 0:
                self.value_normalized = 0
            else:
                self.value_normalized = (x - self.x - padding
                                         ) / float(self.width - 2 * padding)
        else:
            if self.height == 0:
                self.value_normalized = 0
            else:
                self.value_normalized = (y - self.y - padding
                                         ) / float(self.height - 2 * padding)

    value_pos = AliasProperty(get_value_pos, set_value_pos, bind=('pos', 'size', 'min', 'max', 'padding', 'value_normalized', 'orientation'), cache=True)

    def get_loading_value_pos(self):
        padding = self.padding
        x = self.x
        y = self.y
        nval = self.loading_value_normalized
        if self.orientation == 'horizontal':
            return (x + padding + nval * (self.width - 2 * padding), y)
        else:
            return (x, y + padding + nval * (self.height - 2 * padding))

    def set_loading_value_pos(self, loading_pos):
        padding = self.padding
        x = min(self.right - padding, max(loading_pos[0], self.x + padding))
        y = min(self.top - padding, max(loading_pos[1], self.y + padding))
        if self.orientation == 'horizontal':
            if self.width == 0:
                self.loading_value_normalized = 0
            else:
                self.loading_value_normalized = (x - self.x - padding
                                         ) / float(self.width - 2 * padding)
        else:
            if self.height == 0:
                self.loading_value_normalized = 0
            else:
                self.loading_value_normalized = (y - self.y - padding
                                         ) / float(self.height - 2 * padding)

    loading_value_pos = AliasProperty(get_loading_value_pos, set_loading_value_pos, bind=('pos', 'size', 'min', 'max', 'padding', 'loading_value_normalized', 'orientation'), cache=True)

    def on_touch_down(self, touch):
        if self.disabled or not self.collide_point(*touch.pos):
            return
        if touch.is_mouse_scrolling:
            if 'down' in touch.button or 'left' in touch.button:
                if self.step:
                    self.value = min(self.max, self.value + self.step)
                else:
                    self.value = min(
                        self.max,
                        self.value + (self.max - self.min) / 20)
            if 'up' in touch.button or 'right' in touch.button:
                if self.step:
                    self.value = max(self.min, self.value - self.step)
                else:
                    self.value = max(
                        self.min,
                        self.value - (self.max - self.min) / 20)
        elif self.sensitivity == 'handle':
            if self.children[0].collide_point(*touch.pos):
                touch.grab(self)
        else:
            touch.grab(self)
            self.value_pos = touch.pos
        return True

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            self.value_pos = touch.pos
            # self.loading_value_pos = touch.pos[0] - 10, touch.pos[1]
            return True

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            self.value_pos = touch.pos
            return True

class FlexProgressBar(Widget):
    value = NumericProperty(0)
    min = NumericProperty(1)
    max = NumericProperty(100)
    radius = ListProperty([5])
    size_y = NumericProperty(24)

    bg_color = ListProperty([1,1,1,1])
    bar_color = ListProperty([.2,.2,1,1])

    _bg_color = ObjectProperty(None)
    _bar_color = ObjectProperty(None)
    bg_rect = ObjectProperty(None)
    bar_rect = ObjectProperty(None)

    def __init__(self, **kwargs):
        self._value = 0.
        super().__init__(**kwargs)
        self.value = kwargs.get("value", self.value)
        self.max = kwargs.get("max", self.max)
        self.min = kwargs.get("min", self.min)

        with self.canvas.before:
            self._bg_color = Color(rgba=self.bg_color)
            self.bg_rect = RoundedRectangle(
                pos=[self.x, self.center_y - 12], 
                radius=self.radius, 
                size=[self.width, self.size_y])
            self._bar_color = Color(rgba=self.bar_color)
            self.bar_rect = RoundedRectangle(
                pos=[self.x, self.center_y - 12], 
                radius=self.radius, 
                size=[self.width * (self.value / float(self.max)) if self.max else 0, self.size_y])

        self.bind(
            value=self.draw, width=self.draw, height=self.draw,
            bg_color=self.draw, bar_color=self.draw)

    def draw(self, *args):
        self._bg_color.rgba = self.bg_color
        self.bg_rect.pos = [self.x, self.center_y - 12]
        self.bg_rect.radius = self.radius
        self.bg_rect.size = [self.width, self.size_y]

        self._bar_color.rgba = self.bar_color
        self.bar_rect.pos = [self.x, self.center_y - 12]
        self.bar_rect.radius = self.radius
        self.bar_rect.size = [
            self.width * (self.value / float(self.max)) \
                if self.max else 0, self.size_y]

Builder.load_string("""
# <TrackLoadProgressBar>: #TODO #TOREVISE
    # canvas:
    #     Color:
    #         rgba: root.bar_color
    #     RoundedRectangle:
    #         radius: root.radius
    #         pos: root.pos[0] + self.padding / 2, root.pos[1]
    #         # pos: self.x + self.padding / 2, self.center_y - 12
    #         size: root.size[0] - self.padding, root.size[1] / 3
    #     Color:
    #         rgba: root.loading_value_track_color if self.loading_value_track and self.orientation == 'horizontal' else [1, 1, 1, 0]
    #     Line:
    #         width: self.value_track_width
    #         points: self.x + self.padding, self.center_y - self.height / 3, self.loading_value_pos[0], self.center_y - self.height / 3
    #     Color:
    #         rgba: root.value_track_color if self.value_track and self.orientation == 'horizontal' else [1, 1, 1, 0]
    #     Line:
    #         width: self.value_track_width
    #         points: self.x + self.padding - dp(2), self.center_y - self.height / 3, self.value_pos[0], self.center_y - self.height / 3
    #     Color:
    #         rgba: root.value_track_color if self.value_track and self.orientation == 'vertical' else [1, 1, 1, 0]
    #     Line:
    #         width: self.value_track_width
    #         points: self.center_x, self.y + self.padding, self.center_x, self.value_pos[1]
    #     Color:
    #         rgb: 1, 1, 1
    # Widget:
    #     canvas.before:
    #         Color:
    #             rgba: root.cursor_color
    #         RoundedRectangle:
    #             pos: (root.value_pos[0] - root.cursor_width / 2, root.center_y - (root.cursor_height / 2 + root.height / 3)) if root.orientation == 'horizontal' else (root.center_x - root.cursor_width / 2, root.value_pos[1] - root.cursor_height / 2)
    #             size: root.cursor_size
    #             radius: root.cursor_radius

<-TrackLoadProgressBar>:
    centralize: 4
    value_track_width: '6dp'
    canvas:
        Color:
            rgba: root.bar_color
        RoundedRectangle:
            radius: root.radius
            pos: [self.x + self.padding / 2, self.center_y - 12]
            size: [root.size[0] - self.padding, self.value_track_width + 10]
        Color:
            rgba: root.loading_value_track_color \
                  if self.loading_value_track and self.orientation == 'horizontal' \
                  else [1, 1, 1, 0]
        Line:
            width: self.value_track_width
            points: [self.x + self.padding, \
                     self.center_y - self.centralize, \
                     self.loading_value_pos[0], \
                     self.center_y - self.centralize]
        Color:
            rgba: root.value_track_color \
                if self.value_track and self.orientation == 'horizontal' \
                else [1, 1, 1, 0]
        Line:
            width: self.value_track_width
            points: [self.x + self.padding - dp(2), \
                     self.center_y - self.centralize, \
                     self.value_pos[0], \
                     self.center_y - self.centralize]
        Color:
            rgba: root.value_track_color \
                  if self.value_track and self.orientation == 'vertical' \
                  else [1, 1, 1, 0]
        Line:
            width: self.value_track_width
            points: [self.center_x, \
                     self.center_y - self.centralize, \
                     self.center_x, \
                     self.center_y - self.centralize]
        Color:
            rgb: 1, 1, 1
    Widget:
        canvas.before:
            Color:
                rgba: root.cursor_color
            RoundedRectangle:
                pos: (root.value_pos[0] - root.cursor_width / 2, self.parent.center_y-15) \
                      if root.orientation == 'horizontal' \
                      else (root.center_x - root.cursor_width / 2, root.value_pos[1] - root.cursor_height / 2)
                size: root.cursor_size
                radius: root.cursor_radius

<FlexProgressBar>:
""")

if __name__ == '__main__':
    from kivy.app import App
    from kivy.core.window import Window
    Window.size = (320,400)
    from kivy.uix.boxlayout import BoxLayout

    class Main(App):
        tpb = None
        cpb = None
        fpb = None

        # Simple animation to show the circular progress bar in action
        def animate(self, dt):
            if self.tpb.value < 100:
                self.tpb.value += 1
                self.tpb.loading_value += 3
                self.cpb.set_value(self.tpb.value)
                self.fpb.value = self.tpb.value
            else:
                self.tpb.value = 0
                self.tpb.loading_value = 0
                self.cpb.set_value(self.tpb.value)
                self.fpb.value = 0

        def build(self):
            root = BoxLayout(orientation="vertical")

            self.tpb = TrackLoadProgressBar(size_hint_y=.1, min=0, max=100, value=20)
            self.cpb = CircularProgressBar(size_hint_y=.8, min=0, max=100, value=50)
            self.fpb = FlexProgressBar(size_hint_y=.1, min=0, max=100, value=50)

            root.add_widget(self.tpb)
            root.add_widget(self.cpb)
            root.add_widget(self.fpb)

            # Animate the progress bar
            Clock.schedule_interval(self.animate, 0.1)
            return root

    Main().run()