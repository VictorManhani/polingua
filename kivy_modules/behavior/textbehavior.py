from kivy.clock import Clock
from kivy.event import EventDispatcher
from pprint import PrettyPrinter
from kivy.properties import (
    BooleanProperty, ObjectProperty, 
    ListProperty, NumericProperty
)
from print_dict.print_dict import format_dict

class Prettify(EventDispatcher):
    pp = ObjectProperty(None)
    _data = None
    data = ObjectProperty(allownone=True)
    wid = NumericProperty(100)
    depth = NumericProperty(20)
    indent = NumericProperty(2)
    compat = BooleanProperty(False)
    sort_dicts = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.indent = kwargs.get("indent", self.indent)
        self.wid = kwargs.get("wid", self.wid)
        self.depth = kwargs.get("depth", self.depth)
        self.compat = kwargs.get("compat", self.compat)
        self.sort_dicts = kwargs.get("sort_dicts", self.sort_dicts)

        self.pp = PrettyPrinter(
            stream=self, indent=self.indent, 
            width=self.wid, depth=self.depth, 
            compact=self.compat, sort_dicts=self.sort_dicts)
        
        self._data = kwargs.get("data", self.data)
        Clock.schedule_once(self.start)

    def start(self, evt):
        if self.data:
            if self._data:
                self.data = self._data
                self.on_data(self, self.data)

    def write(self, *args):
        self.text += args[0]

    def ppri(self):
        if self.pp:
            if self.data:
                # self.pp.pprint(self.data)
                # TODO change this external method to local method or create one stylish.
                self.text = format_dict(self.data)
                # text = "{"
                # for key in self.data:
                #     format_dict()

                # self.text = 

    def on_data(self, obj, val):
        self.ppri()

    def on_indent(self, obj, val):
        self.ppri()

    def on_wid(self, obj, val):
        self.ppri()

    def on_depth(self, obj, val):
        self.ppri()

    def on_compat(self, obj, val):
        self.ppri()

    def on_sort_dicts(self, obj, val):
        self.ppri()