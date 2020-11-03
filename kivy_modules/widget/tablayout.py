
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
Window.size = [500, 500]

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from kivy.properties import (
    ObjectProperty, ListProperty, NumericProperty, BooleanProperty, StringProperty,
    DictProperty
)

from kivy.graphics import Canvas, Rectangle, Color, RoundedRectangle
from kivy.metrics import dp, sp

import random

class TabItem(BoxLayout):
    text = StringProperty('')
    background_color = ListProperty([.2, .2, .2, 1])
    
class TabLayout(BoxLayout):
    _addresses = ListProperty([])
    _multicolor = BooleanProperty(False)
    _default_color = ListProperty([.2, .2, 1, 1])
    _tab_items = {}
    _menu_items = {}
    _content_items = {}
    _button_name = {}
    _layout_colors = {}

    def __init__(self, *args, **kwargs):
        super(TabLayout, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.inicial_config)
        Clock.schedule_once(self.tab_item, .1)
        Clock.schedule_once(self.colorize, .2)
        Clock.schedule_once(self.item_build, .3)
        Clock.schedule_once(self.tab_manager, .4)

    # Fazer as configurações iniciais após a renderização dos widgets
    def inicial_config(self, evt):
        self.container = self.ids.container
        self.manager = self.ids.manager

    # cria botão personalizado para o menu
    def button_build(self, identifier, text):
        but = Button(
            text = text,
            size_hint = [1, None],
            height = dp(50),
            background_color = [.2, .2, .2, 1],
            background_normal = '',
            halign = "center",
            valign = "middle"
        )
        but.identifier = identifier
        but.text_size = but.size
        but.bind(on_release = self.switch)
        return but

    # obtém os items declarados na tab
    def tab_item(self, evt):
        # Copia endereços dos _tab_items declarados no kv file.
        self._addresses = [tab_i for tab_i in self.children if type(tab_i) is TabItem][::-1]

        # preenche b_utton_name com sueus respectivos nomes e objetos
        for i, a in enumerate(self._addresses):
            # Cria os botões personalizados para o menu
            identifier = f'screen{i}'
            # verifica se o tab_item está sem nome e o nomeia
            if a.text == '':
                a.text = identifier
            # Guarda o nome e o objeto de cada tab_item
            self._tab_items[identifier] = a
            # guarda cada button identificado pelo seu identificador em um dict
            self._menu_items[identifier] = self.button_build(
                identifier, a.text
            )

    # Define as cores dos botões e screebs.
    def colorize(self, evt):
        for i, a in enumerate(self._addresses):
            # Cria os botões personalizados para o menu
            identifier = f'screen{i}'
            # adiciona a cor do tab_item ao dict layoutcolors
            # self._layout_colors[identifier] = a.background_color
            
            if self._multicolor:
                # adiciona cor aleatória ao dict._layout_colors
                self._layout_colors[identifier] = [
                    random.random(), random.random(), random.random(), 1
                ]
            elif not self._multicolor:
                # adiciona a cor padrão ao dict._layout_colors
                self._layout_colors[identifier] = self._default_color

    # Fazer a gestão dos botões como toggle button e das screens
    def switch(self, but):
        if but.background_color == [.2,.2,.2,1]:
            for b in self.container.children:
                b.background_color = [.2,.2,.2,1]
            but.background_color = self._layout_colors[but.identifier]
            self.manager.current = but.identifier

    # criar conteúdo para a content screen
    def screen_build(self, identifier, text, color):
        screen = Builder.load_string(f"""
Screen:
    name: "{identifier}"
    background_color: {color}
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: root.background_color
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [5,]
""")
        return screen

    # preenche o menu e a content screen com items de estrutura.
    def item_build(self, evt):
        for identifier, text in enumerate(self._tab_items):
            # rename the identifier
            identifier = f"screen{identifier}"

            # Adicionar o botão no container
            self.container.add_widget(self._menu_items[identifier])

            # cria as screens personalizadas para a content screen
            self._content_items[identifier] = self.screen_build(
                identifier, text, self._layout_colors[identifier]
            )
            
            # adicionar cor ao tab_item
            self._tab_items[identifier].background_color = self._layout_colors[identifier]
            
            # adicionar a screen criada na screen content
            self.manager.add_widget(self._content_items[identifier])

        # Colore o primeiro botão
        self._menu_items['screen0'].background_color = self._layout_colors['screen0']

    # Preenche cada screen da content screen com os tab_item,
    def tab_manager(self, obj):
        for k, v in self._tab_items.items():
            self.remove_widget(v)
            self._content_items[k].add_widget(v)

Builder.load_string("""
#:import NoTransition kivy.uix.screenmanager.NoTransition

<TabLayout>:
    BoxLayout:
        size_hint: [.2, 1]
        ScrollView:
            do_scroll_y: True
            do_scroll_x: False
            canvas.before:
                Color:
                    rgba: [.25, .25, .25, 1]
                Rectangle:
                    pos: self.pos
                    size: self.size
            BoxLayout:
                id: container 
                orientation: "vertical"
                #padding: 5
                #spacing: 5
                size_hint: [1, None]
                height: self.minimum_height
    BoxLayout:
        size_hint: [.8, 1]
        ScreenManager:
            id: manager
            transition: NoTransition()
            direction: 'right'

<TabItem>:
    # background_color: [.2, .2, .2, 1]
    canvas.before:
        Color:
            rgba: root.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
""")