from src.helpers.imports import *

class Lang1(Screen):
    pass

Builder.load_string("""
<Lang1>:
    FlexLayout:
        padding: [10,30]
        FlexLabel:
            text: "Language 1"
            size_hint: [1,.1]
        FlexButton:
            text: "Love"
            size_hint: [1,.9]
            font_size: sp(30)
            on_release:
                app.switch_screen("lang2", "left", transition="RiseInTransition")
""")
