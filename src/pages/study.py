from src.helpers.imports import *

from plyer import tts
from difflib import SequenceMatcher
from kivy_modules.widget.label import FlexLabel
from kivy_modules.widget.button import FlexIconButton

class Study(Screen):
    app = None
    studied = []
    key = ""
    hit_point = NumericProperty(0)
    miss_point = NumericProperty(0)

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
        self.hit_point += 1
        self.ids.attempt.text = ""

    def miss(self):
        self.rand()
        self.miss_point += 1
        self.ids.attempt.text = ""

    def send_answer(self, answer):
        correct_answers = [word.strip() for word in self.app.store[self.key]["pt"].strip().split(",")]
        
        if answer in correct_answers:
            self.hit()
        elif answer not in correct_answers:
            for c_a in correct_answers:
                result = self.levenshtein(answer, c_a)
                # print(result, result/len(c_a)) # LEVENSHTEIN
                # print((len(c_a) - self.lcs(answer, c_a)[0]) < 3) #LCS (MY IMPLEMENT)
                # print(SequenceMatcher(None, answer, c_a).ratio()) #LCS (BUILTIN)
                if result < 3:
                    self.hit()
                    break
            else:
                self.miss()

    def levenshtein(self, s1, s2):
        if len(s1) > len(s2):
            s1, s2 = s2, s1

        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2+1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        return distances[-1]

    def lcs(self, s1, s2):
        matrix = [["" for x in range(len(s2))] for x in range(len(s1))]

        for i in range(len(s1)):
            for j in range(len(s2)):
                if s1[i] == s2[j]:
                    if i == 0 or j == 0:
                        matrix[i][j] = s1[i]
                    else:
                        matrix[i][j] = matrix[i-1][j-1] + s1[i]
                else:
                    matrix[i][j] = max(matrix[i-1][j], matrix[i][j-1], key=len)

        cs = matrix[-1][-1]

        return len(cs), cs

Builder.load_string("""
<Study>:
    FlexLayout:
        padding: [2,2]
        FlexLabel:
            text: "Study"
            size_hint: [1,.1]
        FlexLayout:
            orientation: "horizontal"
            size_hint: [1,.1]
            FlexLabel:
                text: "miss"
                size_hint: [.25,1]
            FlexLabel:
                text: str(root.miss_point)
                size_hint: [.25,1]
                bg_color: [.8,.1,.3,1]
                fg_color: [1,1,1,1]
            FlexLabel:
                text: "hit"
                size_hint: [.25,1]
            FlexLabel:
                text: str(root.hit_point)
                size_hint: [.25,1]
                bg_color: [.1,.8,.3,1]
                fg_color: [1,1,1,1]
        PageLayout:
            size_hint: [1,.6]
            orientation: "horizontal"
            border: 5
            anim_kwargs: {"d": .1, "t": "out_bounce"}
            FlexLayout:
                FlexLayout:
                    orientation: "horizontal"
                    size_hint: [1, .1]
                    padding: 0
                    # spacing: 0
                    FlexIconButton:
                        icon: "turtle"
                        on_release:
                            app.reproduce(en.text, "en")
                    FlexIconButton:
                        icon: "volume-high"
                        on_release:
                            app.reproduce(en.text, "en")
                FlexButton:
                    id: en
                    text: "English"
                    size_hint: [1, .9]
                    on_release:
                        self.parent.parent.page = 1
            FlexLayout:
                FlexIconButton:
                    icon: "cellphone-sound"
                    size_hint: [1, .1]
                    on_release:
                        app.reproduce(pt.text, "pt")
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
                id: attempt
                size_hint_x: .9
                hint_text: "attempt translation"
            FlexIconButton:
                size_hint_x: .1
                icon: "send"
                on_release:
                    root.send_answer(attempt.text)
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
