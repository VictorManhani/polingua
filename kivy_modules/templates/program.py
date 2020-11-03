default_program = """\
ScreenManager:
    Screen:
        name: "splash"
        FlexLayout:
            orientation: "vertical"
            padding: [5,5]
            FlexLabel:
                text: "Splash"
                size_hint: [1,.1]
            FlexButton:
                text: "Go To Home"
                size_hint: [1,.9]
                on_release:
                    app.switch_screen("home", "left", manager=root)
    Screen:
        name: "home"
        FlexLayout:
            orientation: "vertical"
            padding: [5,5]
            FlexLabel:
                text: "Home"
                size_hint: [1,.1]
            FlexButton:
                text: "Go To Splash"
                size_hint: [1,.9]
                on_release:
                    app.switch_screen("splash", "right", manager=root)
"""

simple_program = """\
ScreenManager:
    Screen:
        FlexLayout:
            FlexButton:
                text: "Hello World"
                on_release:
                    print(self.text)
"""

map_program = """\
ScreenManager:
    Screen:
        FlexLayout:
            FlexLabel:
                text: "Map"
                size_hint: [1,.1]
            FlexButton:
                text: "Get Map"
                size_hint: [1,.9]
                on_release:
                    print(self.text)
"""

parts = {"simple": simple_program, "default": default_program, "map": map_program}