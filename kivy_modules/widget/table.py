from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from ..behavior.ripplebehavior import CircularRippleBehavior, RectangularRippleBehavior
from ..behavior.hoverbehavior import HoverBehavior

from kivy.metrics import sp, dp
from kivy.properties import (
    ListProperty, NumericProperty, StringProperty, 
    OptionProperty, BooleanProperty, ObjectProperty
)

class FlexSelectableRecycleGridLayout(FocusBehavior, 
    LayoutSelectionBehavior, RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''

class FlexSelectableLabel(RecycleDataViewBehavior, RectangularRippleBehavior, HoverBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    
    color = ListProperty([.2,.2,.2,1])
    fg_color = ListProperty([.2,.2,.2,1])
    selected_bg_color = ListProperty([.2,.2,.6,1])
    unselected_bg_color = ListProperty([.2,.2,.8,1])
    hover_color = ListProperty([.2,.2,.7,1])
    unhover_color = ListProperty([.2,.2,.8,1])
    border_color = ListProperty([0.0, 0.4471, 0.8235, 1])
    ripple_color = ListProperty([0.0, 0.6784, 0.9569, 1])
    
    radius = ListProperty([5])
    ripple_duration_in_fast = NumericProperty(0.2)
    font_size = NumericProperty(sp(12))
    border_weigth = ListProperty([1,1,1,1])
    
    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(FlexSelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_enter(self, *args):
        self.unselected_bg_color = self.hover_color
    
    def on_leave(self):
        self.unselected_bg_color = self.unhover_color

    def on_fg_color(self, inst, val):
        self.color = val

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(FlexSelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, tb, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        # if is_selected:
        #     print("selection changed to {0}".format(tb.data[index]))
        #     print(index, tb.data[index])
        # else:
        #     print("selection removed for {0}".format(tb.data[index]))

class FlexSelectableButton(RecycleDataViewBehavior, Button):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(FlexSelectableButton, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(FlexSelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, tb, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

class FlexRV(RecycleView):
    def __init__(self, **kwargs):
        super(FlexRV, self).__init__(**kwargs)

class FlexTable(BoxLayout):
    radius = ListProperty([5])
    bg_color = ListProperty([0.933, 0.933, 0.933, 1])
    # header_color = ListProperty([0.933, 0.933, 0.933, 1])
    # rows_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(FlexTable, self).__init__(**kwargs)

Builder.load_string('''
<FlexSelectableLabel>:
    halign: "center"
    valign: "middle"
    text_size: root.size
    canvas.before:
        Color:
            rgba: root.selected_bg_color if self.selected else root.unselected_bg_color
        Rectangle:
            pos: root.pos
            size: root.size

<FlexRV>:
    viewclass: 'FlexSelectableLabel'
    FlexSelectableRecycleGridLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: True
        touch_multiselect: True
        cols: 3

<FlexTable>:
    rv: root.children[0]
    canvas.before:
        Color:
            rgba: root.bg_color
        RoundedRectangle:
            pos: root.pos
            size: root.size
            radius: root.radius
    FlexRV:
''')

if __name__ == '__main__':
    class TestApp(App):
        def build(self):
            self.table = FlexTable()
            self.table.rv.layout_manager.bind(
                selected_nodes=self.selection_change)

            colums = ["action", "music name", "status"]
            header_color = [0.933, 0.933, 0.933, 1]
            data = [(c, header_color) for c in colums]
            
            items =  ["play", "hillsong - oceans", "download", 
                      "stop", "hillsong - broken vessels", "downloaded",
                      "play", "tasha cobbs - fill me up", "downloaded", 
                      "play", "lauren daigle - you say", "downloaded"]
            rows_color = [1, 1, 1, 1]
            data += [(c, rows_color) for c in items]

            # self.table.rv.viewclass = "FlexSelectableButton"
            self.table.rv.data = [{
                'text': str(x[0]), 'selected_bg_color': x[1]} for x in data]
    
            return self.table

        def selection_change(self, instancia, value):
            # print("instancia", instancia)
            # print("value", value)
            print("text", self.table.rv.data[value[-1] if value else 0]['text'])

    TestApp().run()