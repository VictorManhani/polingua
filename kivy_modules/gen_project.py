from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.clock import mainthread
from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.properties import ListProperty

from kivy.core.window import Window
from kivy.utils import platform

if platform not in ["android", "ios"]:
    Window.size = (500,400)

import os
import sys
from distutils.dir_util import copy_tree
import importlib

from templates.program import parts

class Gen:
    current_file_dir = ""
    current_project_dir = ""

    current_work_dir = ""
    old_kivy_dir = ""
    new_kivy_dir = ""

    src_dir = ""
    helpers_dir = ""
    pages_dir = ""
    routes_dir = ""

    def __init__(self, **kwargs):
        pass

    def set_dir(self, project_name):
        self.current_file_dir = os.path.dirname(os.path.abspath(__file__))
        self.current_project_dir = os.path.dirname(self.current_file_dir)

        self.current_work_dir = os.path.join(self.current_project_dir, project_name)

        self.old_kivy_dir = os.path.join(self.current_project_dir, "kivy_modules")
        self.new_kivy_dir = os.path.join(self.current_work_dir, "kivy_modules")

        self.src_dir = os.path.join(self.current_work_dir, "src")
        self.helpers_dir = os.path.join(self.src_dir, "helpers")
        self.pages_dir = os.path.join(self.src_dir, "pages")
        self.routes_dir = os.path.join(self.src_dir, "routes")

    def gen_work_dir(self):
        try:
            os.mkdir(self.current_work_dir)
            os.mkdir(self.src_dir)
            os.mkdir(self.helpers_dir)
            os.mkdir(self.pages_dir)
            os.mkdir(self.routes_dir)
            os.mkdir(self.new_kivy_dir)
            copy_tree(self.old_kivy_dir, self.new_kivy_dir)
        except Exception as e:
            print(str(e))

    def create_file(self, filepath, filename, text):
        with open(os.path.join(filepath, filename), 
                  "w", encoding="UTF-8") as f:
            f.write(text)

    def generate_files(self, type):
        mod = os.path.join(
            "kivy_modules", "templates", type, "gen").replace(os.sep, ".")
        mod = importlib.import_module(mod)

        for part in mod.parts:
            self.create_file(
                getattr(self, f"{mod.parts[part][1]}_dir"), 
                f"{part}.py", 
                mod.parts[part][0])

class Container(Screen):
    spinner_values = ListProperty(["default", "simple", "map"])

    def update_spinner(self):
        tem = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "templates"
        )
        self.ids.spinner.values = list(
            filter(
                lambda x: False if "__" in x or ".py" in x else True, 
                os.listdir(tem)
            )
        )

    def add_container(self, type):
        self.ids.container.clear_widgets()
        kv = parts[type]
        kv = Builder.load_string(kv)
        self.ids.container.add_widget(kv)

    def start_project(self, type, project_name):
        project_name = project_name.replace(' ', '_')
        project_name = project_name.lower()

        gen = Gen()
        gen.set_dir(project_name)
        gen.gen_work_dir()
        gen.generate_files(type)

Builder.load_string("""
<Container>:
    BoxLayout:
        BoxLayout:
            orientation: "vertical"
            size_hint: [.5,1]
            spacing: 5
            padding: 5
            Spinner:
                id: spinner
                text: "default"
                values: root.spinner_values
                size_hint: [1,.1]
                on_text:
                    root.add_container(spinner.text)
                    root.update_spinner()
            TextInput:
                id: project_name
                text: "My Project"
                hint_text: "Project Name"
                size_hint: [1,.1]
            TextInput:
                text: "Victor"
                hint_text: "Project Author"
                size_hint: [1,.1]
            Button:
                text: "Start Project"
                size_hint: [1,.1]
                on_release:
                    root.start_project(spinner.text, project_name.text)
            Widget:
                size_hint: [1,.6]
        BoxLayout:
            id: container
            size_hint: [.5,1]
            orientation: "vertical"

<Manager>:
    Container:
        name: "container"
""")

class Manager(ScreenManager):
    pass

class TemplateApp(App):
    title = "Template"

    @mainthread
    def switch_screen(self, screen, direction, manager=None):
        """If not a manager, it uses the major manager as default."""
        if manager:
            manager.transition.direction = direction
            manager.current = screen
            return
        self.root.transition.direction = direction
        self.root.current = screen

    def build(self):
        current_dir = os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))

        sys.path.append(current_dir)

        Factory.register('FlexLayout', module='kivy_modules.widget.layout')
        Factory.register('FlexButton', module='kivy_modules.widget.button')
        Factory.register('FlexLabel', module='kivy_modules.widget.label')

        return Manager()

TemplateApp().run()