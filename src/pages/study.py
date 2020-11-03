from src.helpers.imports import *

from plyer import tts

class Study(Screen):
    app = None
    studied = []
    key = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def rand(self):
        self.key = random.choice(list(self.app.store.keys()))

        while self.key in self.studied:
            self.key = random.choice(list(self.app.store.keys()))
            if len(self.app.store) == len(self.studied):
                return

        self.ids.en.text = self.app.store[self.key]["en"]
        self.ids.pt.text = self.app.store[self.key]["pt"]

    def hit(self):
        self.studied.append(self.key)
        self.rand()

    def miss(self):
        # self.studied.append(self.key)
        self.rand()

Builder.load_string("""
<Study>:
    FlexLayout:
        padding: [2,2]
        FlexLabel:
            text: "Study"
            size_hint: [1,.1]
        PageLayout:
            size_hint: [1,.7]
            orientation: "horizontal"
            border: 5
            anim_kwargs: {"d": .1, "t": "out_bounce"}
            FlexLayout:
                IconButton:
                    icon: "cellphone-sound"
                    size_hint: [1, .1]
                    on_release:
                        reproduce(en.text, "en")
                FlexButton:
                    id: en
                    text: "English"
                    size_hint: [1, .9]
                    on_release:
                        self.parent.parent.page = 1
            FlexLayout:
                IconButton:
                    icon: "cellphone-sound"
                    size_hint: [1, .1]
                    on_release:
                        reproduce(pt.text, "pt")
                FlexButton:
                    id: pt
                    text: "Portuguese"
                    size_hint: [1, .9]
                    on_release:
                        self.parent.parent.page = 0
        FlexLayout:
            orientation: "horizontal"
            size_hint: [1,.1]
            FlexText:
                size_hint_x: .9
                text_hint: "attempt"
            IconButton:
                size_hint_x: .1
                icon: "send"
        FlexLayout:
            orientation: "horizontal"
            size_hint: [1,.1]
            FlexButton:
                text: "<-"
                on_release:
                    app.switch_screen("home", "right")
            FlexButton:
                text: "No" # TODO
                on_release:
                    root.miss()
            FlexButton:
                text: "Yes" # TODO
                on_release:
                    root.hit()
""")
