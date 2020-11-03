from src.helpers.imports import *

class Lang2(Screen):
    pass

Builder.load_string("""
<Lang2>:
    FlexLayout:
        padding: [10,30]
        FlexLabel:
            text: "Language 2"
            size_hint: [1,.1]
        FlexButton:
            text: "Amor"
            size_hint: [1,.9]
            font_size: sp(30)
            on_release:
                app.switch_screen("lang1", "right", transition="FallOutTransition")
""")
