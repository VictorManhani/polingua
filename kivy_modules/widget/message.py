from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock

from kivy.properties import StringProperty, ListProperty

class SaveMessage(Popup):
    size_hint = ListProperty([1, .3])
    saved = StringProperty()

    def __init__(self, my_widget=Button(text = "My Widget"),**kwargs):  # my_widget is now the object where popup was called from.
        super(SaveMessage, self).__init__(**kwargs)
        self.my_widget = my_widget
        Clock.schedule_once(self.start, .1)

    def start(self, evt):
        self.title = "Save Dialog"

        self.all_content = BoxLayout(orientation = "vertical")

        boxlayout_text = BoxLayout(orientation = "vertical", size_hint = [1, .6])
        self.info = TextInput(hint_text = "some text here")
        boxlayout_text.add_widget(self.info)

        boxlayout_button = BoxLayout(orientation = "horizontal", size_hint = [1, .4])
        self.save_button = Button(text = 'Save')
        self.save_button.bind(on_press = self.save)
        self.cancel_button = Button(text = 'Cancel')
        self.cancel_button.bind(on_press = self.cancel)
        boxlayout_button.add_widget(self.cancel_button)
        boxlayout_button.add_widget(self.save_button)

        self.all_content.add_widget(boxlayout_text)
        self.all_content.add_widget(boxlayout_button)
        self.add_widget(self.all_content)

    def save(self,*args):
        self.dismiss()
        self.saved = self.info.text

    def cancel(self,*args):
        self.dismiss()
        return -1
