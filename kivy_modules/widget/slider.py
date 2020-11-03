__all__ = ('FlexSlider', )

import os
import sys
root = os.path.abspath(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.realpath(__file__)))))
sys.path.insert(0,root)

from kivy.lang import Builder
from kivy_modules.widget.widget import Widget
from kivy.properties import (NumericProperty, AliasProperty, OptionProperty,
                             ReferenceListProperty, BoundedNumericProperty,
                             StringProperty, ListProperty, BooleanProperty)

# oldcwd = os.getcwd()
# os.chdir(path)
# module_name = "..__init__"
# class_name = "Builder"
# # klass = getattr(__import__(module_name), class_name)
# # print(klass)
# print(os.listdir())
# mod = __import__(module_name)
# print(mod)

class FlexSlider(Widget):
    value = NumericProperty(0.)
    min = NumericProperty(0.)
    max = NumericProperty(100.)
    padding = NumericProperty('16sp') # default: 16sp
    orientation = OptionProperty('horizontal', options=(
        'vertical', 'horizontal'))
    range = ReferenceListProperty(min, max)
    step = BoundedNumericProperty(0, min=0)
    background_horizontal = StringProperty(
        'atlas://data/images/defaulttheme/sliderh_background')
    background_disabled_horizontal = StringProperty(
        'atlas://data/images/defaulttheme/sliderh_background_disabled')
    background_vertical = StringProperty(
        'atlas://data/images/defaulttheme/sliderv_background')
    background_disabled_vertical = StringProperty(
        'atlas://data/images/defaulttheme/sliderv_background_disabled')
    background_width = NumericProperty('36sp')
    cursor_image = StringProperty(
        'atlas://data/images/defaulttheme/slider_cursor')
    cursor_disabled_image = StringProperty(
        'atlas://data/images/defaulttheme/slider_cursor_disabled')
    cursor_width = NumericProperty('32sp')
    cursor_height = NumericProperty('32sp')
    cursor_size = ReferenceListProperty(cursor_width, cursor_height)
    border_horizontal = ListProperty([0, 18, 0, 18])
    border_vertical = ListProperty([18, 0, 18, 0])
    value_track = BooleanProperty(False)
    value_track_color = ListProperty([1, 1, 1, 1])
    value_track_width = NumericProperty('3dp')
    sensitivity = OptionProperty('all', options=('all', 'handle'))

    def on_min(self, *largs):
        self.value = min(self.max, max(self.min, self.value))

    def on_max(self, *largs):
        self.value = min(self.max, max(self.min, self.value))

    def get_norm_value(self):
        vmin = self.min
        d = self.max - vmin
        if d == 0:
            return 0
        return (self.value - vmin) / float(d)

    def set_norm_value(self, value):
        vmin = self.min
        vmax = self.max
        step = self.step
        val = min(value * (vmax - vmin) + vmin, vmax)
        if step == 0:
            self.value = val
        else:
            self.value = min(round((val - vmin) / step) * step + vmin,
                             vmax)

    value_normalized = AliasProperty(get_norm_value, set_norm_value,
                                     bind=('value', 'min', 'max'),
                                     cache=True)

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

    value_pos = AliasProperty(get_value_pos, set_value_pos,
                              bind=('pos', 'size', 'min', 'max', 'padding',
                                    'value_normalized', 'orientation'),
                              cache=True)

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
            self.loading_value_pos = touch.pos[0] - 10, touch.pos[1]
            return True

    def on_touch_up(self, touch):
        if touch.grab_current == self:
            self.value_pos = touch.pos
            return True

Builder.load_string("""
<FlexSlider>:
    canvas:
        Color:
            rgb: 1, 1, 1
        RoundedRectangle:
            radius: self.border_horizontal if self.orientation == 'horizontal' else self.border_vertical
            pos: (self.x + self.padding, self.center_y - self.background_width / 2) if self.orientation == 'horizontal' else (self.center_x - self.background_width / 2, self.y + self.padding)
            size: (self.width - self.padding * 2, self.background_width) if self.orientation == 'horizontal' else (self.background_width, self.height - self.padding * 2)
        Color:
            rgba: root.value_track_color if self.value_track and self.orientation == 'horizontal' else [1, 1, 1, 0]
        Line:
            width: self.value_track_width
            points: self.x + self.padding, self.center_y - self.value_track_width / 2, self.value_pos[0], self.center_y - self.value_track_width / 2
        Color:
            rgba: root.value_track_color if self.value_track and self.orientation == 'vertical' else [1, 1, 1, 0]
        Line:
            width: self.value_track_width
            points: self.center_x, self.y + self.padding, self.center_x, self.value_pos[1]
        Color:
            rgb: 1, 1, 1
    Label:
        canvas:
            Color:
                rgb: 0, 1, 1
            RoundedRectangle:
                pos: (root.value_pos[0] - root.cursor_width / 2, root.center_y - root.cursor_height / 2) if root.orientation == 'horizontal' else (root.center_x - root.cursor_width / 2, root.value_pos[1] - root.cursor_height / 2)
                size: root.cursor_size
""")

if __name__ == '__main__':
    from kivy.app import App

    class FlexSliderApp(App):
        def build(self):
            return FlexSlider(padding=25,
                              value_track = True,
                              value_track_color = [1,0,0,1])

    FlexSliderApp().run()