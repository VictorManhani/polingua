from src.helpers.imports import *

class Wordboard(Screen):
    app = None
    rows = NumericProperty(1)
    row_height = 60

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def get_translation(self, obj):
        if obj.text in self.app.store:
            self.app.root.get_screen("home").ids.en.text = self.app.store[obj.text]["en"]
            self.app.root.get_screen("home").ids.pt.text = self.app.store[obj.text]["pt"]
            self.app.switch_screen("home", "left")

    def load_list(self, words):
        self.ids.en.clear_widgets()
        self.ids.pt.clear_widgets()

        self.rows = len(words)

        for word in words:
            pt_text = words[word]["pt"]
            pt_text = pt_text[:31]+"..." if len(pt_text) > 31 else pt_text

            en = FlexButton(text = word)
            pt = FlexButton(text = pt_text)

            pt.size_hint_y = None
            pt.height = self.row_height

            en.size_hint_y = None
            en.height = self.row_height

            pt.text_size = [pt.width + 50, pt.height]

            en.bind(on_release = self.get_translation)

            self.ids.en.add_widget(en)
            self.ids.pt.add_widget(pt)

    def search(self, text):
        words = {k:self.app.store[k] for k in self.app.store if text in k}
        if text:
            self.load_list(words)
        else:
            self.load_list(self.app.store)     

Builder.load_string("""
<Wordboard>:
    FlexLayout:
        padding: [5,5]
        FlexLabel:
            text: "Wordboard"
            size_hint: [1,.1]
        FlexLayout:
            orientation: "horizontal"
            size_hint: [1,.1]
            FlexText:
                hint_text: "Search"
                size_hint_x: 1
                on_text:
                    root.search(self.text)
        FlexLayout:
            orientation: "horizontal"
            size_hint: [1,.7]
            ScrollView:
                id: scroll_en
                scroll_y: scroll_pt.scroll_y
                effect_cls: "ScrollEffect"
                bar_color: [1,1,1,0]
                GridLayout:
                    id: en
                    cols: 1
                    rows: root.rows
                    size_hint: [1,None]
                    height: self.minimum_height
                    # row_force_default: True
                    # row_default_height: dp(root.row_height)
                    spacing: 1
            ScrollView:
                id: scroll_pt
                scroll_y: scroll_en.scroll_y
                effect_cls: "ScrollEffect"
                bar_color: app.style_color["first_body_color"]
                GridLayout:
                    id: pt
                    cols: 1
                    rows: root.rows
                    size_hint: [1,None]
                    height: en.minimum_height
                    # row_force_default: True
                    # row_default_height: dp(root.row_height)
                    spacing: 1
        FlexLayout:
            orientation: "horizontal"
            size_hint: [1,.1]
            FlexButton:
                text: "Home"
                on_release:
                    app.switch_screen("home", "left")
""")
