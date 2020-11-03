from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from functools import partial

from datetime import datetime
import calendar
from math import ceil

class FlexCalendar(GridLayout):
    now = datetime.now()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(partial(self.update_calendar, self.now.year, self.now.month), .5)

    def update_calendar(self, year, month, *obj):
        print(year, month)
        
        self.clear_widgets()
        
        if year and month:
            year = int(year)
            month = int(month)
        else:
            year = self.now.year
            month = self.now.month
        
        monthrange = calendar.monthrange(year, month)
        self.rows = ceil((monthrange[1] + monthrange[0] + 1) / 7) + 1
        self.cols = 7

        cal = calendar.Calendar(calendar.SUNDAY)
        days = [day for day in ['Su','Mo','Tu','We','Th','Fr','Sa']] + [day for day in cal.itermonthdays(year, month)]
        
        for dia in days:
            color = [1, .2, .2, 1] if dia == self.now.day else [.9, .9, .9, 1]
            dia = '' if dia == 0 else str(dia)
            
            self.add_widget(
                Button(
                    text = dia,
                    color = [.2, .2, .2, 1],
                    background_normal = '',
                    background_color = color
                )
            )

if __name__ == "__main__":
    class MainApp(App):
        title = "Kivy Calendar"
        
        def build(self):
            kv = Builder.load_string("""
    BoxLayout:
        orientation: "vertical"
        BoxLayout:
            size_hint: 1, .1
            Spinner:
                id: year
                on_text:
                    calendar.update_calendar(year.text, month.text)
            Spinner:
                id: month
                on_text:
                    calendar.update_calendar(year.text, month.text)
        FlexCalendar:
            id: calendar
            size_hint: 1, .9
    """)
            self.year = kv.ids.year
            self.month = kv.ids.month
            
            now = datetime.now()
            
            self.year.text = str(now.year)
            self.month.text = str(now.month)
            
            self.year.values = [str(year) for year in range(now.year - 10, now.year + 10, 1)]
            self.month.values = [str(month) for month in range(1, 13)]
            
            return kv

    MainApp().run()
