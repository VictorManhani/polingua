from src.helpers.imports import *

class Home(Screen):
    app = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def save(self, en, pt):
        en_text = en.text.strip().lower()
        pt_text = pt.text.strip().lower()

        if not en_text:
            self.ids.info.text = f"English field is void."
            return False

        if not pt_text:
            self.ids.info.text = f"Portuguese field is void."
            return False

        if en_text in self.app.store:
            self.ids.info.text = f"Word [color=#FF0000FF]{en_text}[/color] that means [color=#008800FF]{self.app.store[en_text]['pt']}[/color] already exists."
            return False

        self.app.store[en_text] = {"en": en_text, "pt": pt_text}

        en.text = ""
        pt.text = ""

        self.ids.info.text = f"Word [color=#FF0000FF]{en_text}[/color] that means [color=#008800FF]{self.app.store[en_text]['pt']}[/color] saved with success."

Builder.load_string("""
#:import reproduce src.helpers.helpers.reproduce

<Home>:
    FlexLayout:
        padding: [2,2]
        FlexLabel:
            text: "Save New Word"
            size_hint: [1,.1]
        FlexLayout:
            size_hint: [1,.3]
            orientation: "horizontal"
            FlexText:
                id: en
                hint_text: "English"
                size_hint_x: .8
            FlexButton:
                text: "s"
                size_hint_x: .2
                on_release:
                    reproduce(en.text, "en")
        FlexLayout:
            size_hint: [1,.3]
            orientation: "horizontal"
            FlexText:
                id: pt
                hint_text: "Portuguese"
                size_hint_x: .8
            FlexButton:
                text: "s"
                size_hint_x: .2
                on_release:
                    reproduce(pt.text, "pt-br")
        FlexLabel:
            id: info
            text: "Informations"
            size_hint: [1,.2]
            markup: True
            padding: [5,5]
        FlexLayout:
            orientation: "horizontal"
            size_hint: [1,.1]
            FlexButton:
                text: "Word List"
                on_release:
                    app.root.get_screen("wordboard").load_list(app.store)
                    app.switch_screen("wordboard", "right")
            FlexButton:
                text: "Save"
                on_release:
                    root.save(en, pt)
            FlexButton:
                text: "Study"
                on_release:
                    app.root.get_screen("study").rand()
                    app.switch_screen("study", "left")
""")
