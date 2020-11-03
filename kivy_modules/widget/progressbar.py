from kivy.app import App
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
from kivy.lang.builder import Builder
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.properties import (NumericProperty, AliasProperty, 
                             ListProperty, OptionProperty, BooleanProperty,
                             BoundedNumericProperty, ReferenceListProperty)

import random

class CircularProgressBar(ProgressBar):

    def __init__(self, **kwargs):
        super(CircularProgressBar, self).__init__(**kwargs)

        # Set constant for the bar thickness
        self.thickness = 40

        # Create a direct text representation
        self.label = CoreLabel(text="0%", font_size=self.thickness)

        # Initialise the texture_size variable
        self.texture_size = None

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

    value_track_width = NumericProperty('6dp')

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

Builder.load_string("""
<TrackLoadProgressBar>:
    canvas:
        Color:
            rgba: root.bar_color
        RoundedRectangle:
            # radius: self.border_horizontal if self.orientation == 'horizontal' else self.border_vertical # 
            # pos: (self.x + self.padding, self.center_y - self.width / 2) if self.orientation == 'horizontal' else (self.center_x - self.width / 2, self.y + self.padding)
            # size: (self.width - self.padding * 2, self.width) if self.orientation == 'horizontal' else (self.width, self.height - self.padding * 2)
            radius: root.radius
            pos: root.pos[0] + self.padding / 2, root.pos[1]
            size: root.size[0] - self.padding, root.size[1] / 3

        # RoundedRectangle:
        #     pos: self.x, self.center_y - 12
        #     size: self.width * (self.value / float(self.max)) if self.max else 0, 24
        #     radius: root.radius
        Color:
            rgba: root.loading_value_track_color if self.loading_value_track and self.orientation == 'horizontal' else [1, 1, 1, 0]
        Line:
            width: self.value_track_width
            points: self.x + self.padding, self.center_y - self.height / 3, self.loading_value_pos[0], self.center_y - self.height / 3
        Color:
            rgba: root.value_track_color if self.value_track and self.orientation == 'horizontal' else [1, 1, 1, 0]
        Line:
            width: self.value_track_width
            points: self.x + self.padding - dp(2), self.center_y - self.height / 3, self.value_pos[0], self.center_y - self.height / 3
        Color:
            rgba: root.value_track_color if self.value_track and self.orientation == 'vertical' else [1, 1, 1, 0]
        Line:
            width: self.value_track_width
            points: self.center_x, self.y + self.padding, self.center_x, self.value_pos[1]
        Color:
            rgb: 1, 1, 1
    Widget:
        canvas.before:
            Color:
                rgba: root.cursor_color
            RoundedRectangle:
                pos: (root.value_pos[0] - root.cursor_width / 2, root.center_y - (root.cursor_height / 2 + root.height / 3)) if root.orientation == 'horizontal' else (root.center_x - root.cursor_width / 2, root.value_pos[1] - root.cursor_height / 2)
                size: root.cursor_size
                radius: root.cursor_radius
""")

class Main(App):
    # Simple animation to show the circular progress bar in action
    def animate(self, dt):
        cpb = self.root.ids["cpb"]
        tlpb = self.root.ids["tlpb"]
        if tlpb.value < 100:
            tlpb.value += 1
            tlpb.loading_value += 3
            cpb.set_value(tlpb.value)
        else:
            tlpb.value = 0
            tlpb.loading_value = 0
            cpb.set_value(tlpb.value)

    # Simple layout for easy example
    def build(self):
        container = Builder.load_string('''
FloatLayout:
    orientation: "vertical"
    canvas.before:
        Color:
            rgba: [0,0,0,1]
        Rectangle:
            pos: self.pos
            size: self.size
    CircularProgressBar:
        id: cpb
        size_hint: None, None
        size: 150, 150
        pos_hint: {"center_x": .5, "center_y": .7}
        max: 100
    BoxLayout:
        size_hint: [1, .1]
        pos_hint: {"center_x": .5, "center_y": .4}
        canvas.before:
            Color:
                rgba: [.2,.2,.2,1]
            Rectangle:
                pos: self.pos
                size: self.size
        TrackLoadProgressBar:
            id: tlpb
            pos_hint: {"center_x": .5, "center_y": .8}
            min: 0
            max: 100
            value: 0
    Widget:
        size_hint: 1, .3
''')

        # Animate the progress bar
        Clock.schedule_interval(self.animate, 0.1)
        return container

if __name__ == '__main__':
    Main().run()