
from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

from kivy.properties import (
    ObjectProperty, ListProperty, NumericProperty, 
    BooleanProperty, StringProperty, DictProperty,
    OptionProperty, AliasProperty
)

from kivy.graphics import Canvas, Rectangle, Color, RoundedRectangle
from kivy.metrics import dp, sp

from kivy.resources import resource_find
import sys
sys.path.insert(0, resource_find('.'))

try:
    from label import FlexLabel
    from button import FlexButton
    from layout import FlexLayout
except:
    from kivy_modules.widget.label import FlexLabel
    from kivy_modules.widget.button import FlexButton
    from kivy_modules.widget.layout import FlexLayout

from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDToolbar
from kivy.core.window import Window
from kivy.logger import Logger
from kivy.animation import Animation, AnimationTransition
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.lang import Builder

class NavigationContainer(FlexLayout):
    orientation = StringProperty("vertical")

class StackNavigator(FlexLayout):
    orientation = StringProperty("vertical")
    title = StringProperty("")
    bg_color = ListProperty([1,1,1,1])
    manager = ObjectProperty()
    current = StringProperty("")
    header_text = ObjectProperty()
    first_screen = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.start)

    def start(self, evt):
        children = self.children[::-1]
        self.clear_widgets()

        # HEADER
        self.header = FlexLayout(
            orientation = "horizontal", size_hint = [1,.1])
        self.header_text = FlexLabel(bold = True)
        self.header.add_widget(self.header_text)
        self.title = children[0].name
        self.first_screen = children[0].name

        # BODY
        self.manager = ScreenManager(size_hint = [1,.9])
        for c in children:
            self.manager.add_widget(c)

        self.add_widget(self.header)
        self.add_widget(self.manager)

    def on_current(self, obj, val):
        self.title = val
        setattr(self.manager, 'current', val)

        if val == self.first_screen:
            setattr(self.manager.transition, 'direction', 'right')
            self.header.clear_widgets()
            self.header.add_widget(self.header_text)
        else:
            setattr(self.manager.transition, 'direction', 'left')
            ib = FlexButton(text = "<-", size_hint = [.15,1])
            ib.bind(on_release = lambda o: [
                setattr(self, 'current', self.first_screen),
                setattr(self.manager.transition, 'direction', 'right')
                ])
            # IconButton(icon = "arrow-left", size_hint = [.1,1])
            self.header.clear_widgets()
            self.header.add_widget(ib)
            self.header.add_widget(self.header_text)

    def on_title(self, obj, val):
        setattr(self.header_text, 'text', val)

class BottomNavigator(FlexLayout):
    orientation = StringProperty("vertical")
    bg_color = ListProperty([1,1,1,1])
    manager = ObjectProperty()
    current = StringProperty("")
    first_screen = StringProperty("")
    footer_color_normal = [.2,.8,1,1]
    footer_color_selected = [1,1,1,1]
    last_index = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.start)

    def start(self, evt):
        children = self.children[::-1]
        self.clear_widgets()

        # FOOTER
        self.footer = FlexLayout(
            orientation = "horizontal", size_hint = [1,.1])

        # BODY
        self.manager = ScreenManager(size_hint = [1,.9])

        for i, c in enumerate(children):
            self.manager.add_widget(c)
            title = c.title if hasattr(c, 'title') else c.name
            b = FlexButton(text = title)
            b.self_screen = c.name
            b.index = i
            if i == 0:
                 b.selected = True
                 b.bg_color = self.footer_color_selected
            else:
                b.selected = False
                b.bg_color = self.footer_color_normal
            b.bind(on_release = self.switch)
            self.footer.add_widget(b)

        self.add_widget(self.manager)
        self.add_widget(self.footer)

    def switch(self, but):
        if not but.selected:
            for b in self.footer.children:
                b.bg_color = self.footer_color_normal
                b.selected = False
            but.bg_color = self.footer_color_selected
            but.selected = True

            self.manager.transition.direction = \
                "left" if but.index > self.last_index else "right"
            self.manager.current = but.self_screen
            self.last_index = but.index

    def on_current(self, obj, val):
        for f in self.footer.children:
            if f.self_screen == val:
                self.switch(f)
                return True


class NavigationDrawerContentError(Exception):
    pass

class NavigationLayout(Factory.FloatLayout):
    _scrim_color = ObjectProperty(None)
    _scrim_rectangle = ObjectProperty(None)

    def add_scrim(self, widget):
        with widget.canvas.after:
            self._scrim_color = Color(rgba=[0, 0, 0, 0])
            self._scrim_rectangle = Rectangle(pos=widget.pos, size=widget.size)
            widget.bind(
                pos=self.update_scrim_rectangle,
                size=self.update_scrim_rectangle,
            )

    def update_scrim_rectangle(self, *args):
        self._scrim_rectangle.pos = self.pos
        self._scrim_rectangle.size = self.size

    def add_widget(self, widget, index=0, canvas=None):
        """
        Only two layouts are allowed:
        :class:`~kivy.uix.screenmanager.ScreenManager` and
        :class:`~MDNavigationDrawer`.
        """

        if not isinstance(
            widget, (DrawerNavigator, ScreenManager, MDToolbar)
        ):
            raise NavigationDrawerContentError(
                "The NavigationLayout must contain "
                "only `MDNavigationDrawer` and `ScreenManager`"
            )
        if isinstance(widget, ScreenManager):
            self.add_scrim(widget)
        if len(self.children) > 3:
            raise NavigationDrawerContentError(
                "The NavigationLayout must contain "
                "only `MDNavigationDrawer` and `ScreenManager`"
            )
        return super().add_widget(widget)

class DrawerNavigator(MDCard):
    bg_color = ListProperty([1,1,1,1])
    anchor = OptionProperty("left", options=("left", "right"))
    close_on_click = BooleanProperty(True)
    state = OptionProperty("close", options=("close", "open"))
    status = OptionProperty(
        "closed",
        options=(
            "closed", "opening_with_swipe", "opening_with_animation",
            "opened", "closing_with_swipe", "closing_with_animation",
        ),
    )
    open_progress = NumericProperty(0.0)
    swipe_distance = NumericProperty(10)
    swipe_edge_width = NumericProperty(20)
    scrim_color = ListProperty([0, 0, 0, 0.5])

    def _get_scrim_alpha(self):
        _scrim_alpha = self._scrim_alpha_transition(self.open_progress)
        if isinstance(self.parent, NavigationLayout):
            self.parent._scrim_color.rgba = self.scrim_color[:3] + [
                self.scrim_color[3] * _scrim_alpha
            ]
        return _scrim_alpha

    _scrim_alpha = AliasProperty(
        _get_scrim_alpha,
        None,
        bind=("_scrim_alpha_transition", "open_progress", "scrim_color"),
    )
    """
    Multiplier for alpha channel of :attr:`scrim_color`. For internal
    usage only.
    """

    scrim_alpha_transition = StringProperty("linear")
    """
    The name of the animation transition type to use for changing
    :attr:`scrim_alpha`.

    :attr:`scrim_alpha_transition` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'linear'`.
    """

    def _get_scrim_alpha_transition(self):
        return getattr(AnimationTransition, self.scrim_alpha_transition)

    _scrim_alpha_transition = AliasProperty(
        _get_scrim_alpha_transition, None,
        bind=("scrim_alpha_transition",), cache=True,
    )

    opening_transition = StringProperty("out_cubic")
    opening_time = NumericProperty(0.2)
    closing_transition = StringProperty("out_sine")
    closing_time = NumericProperty(0.2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            open_progress=self.update_status,
            status=self.update_status,
            state=self.update_status,
        )
        Window.bind(on_keyboard=self._handle_keyboard)

    def set_state(self, new_state="toggle", animation=True):
        """Change state of the side panel.
        New_state can be one of `"toggle"`, `"open"` or `"close"`.
        """

        if new_state == "toggle":
            new_state = "close" if self.state == "open" else "open"

        if new_state == "open":
            Animation.cancel_all(self, "open_progress")
            self.status = "opening_with_animation"
            if animation:
                Animation(
                    open_progress=1.0,
                    d=self.opening_time * (1 - self.open_progress),
                    t=self.opening_transition,
                ).start(self)
            else:
                self.open_progress = 1
        else:  # "close"
            Animation.cancel_all(self, "open_progress")
            self.status = "closing_with_animation"
            if animation:
                Animation(
                    open_progress=0.0,
                    d=self.closing_time * self.open_progress,
                    t=self.closing_transition,
                ).start(self)
            else:
                self.open_progress = 0

    def toggle_nav_drawer(self):
        Logger.warning(
            "KivyMD: The 'toggle_nav_drawer' method is deprecated, "
            "use 'set_state' instead."
        )
        self.set_state("toggle", animation=True)

    def update_status(self, *_):
        status = self.status
        if status == "closed":
            self.state = "close"
        elif status == "opened":
            self.state = "open"
        elif self.open_progress == 1 and status == "opening_with_animation":
            self.status = "opened"
            self.state = "open"
        elif self.open_progress == 0 and status == "closing_with_animation":
            self.status = "closed"
            self.state = "close"
        elif status in (
            "opening_with_swipe",
            "opening_with_animation",
            "closing_with_swipe",
            "closing_with_animation",
        ):
            pass

    def get_dist_from_side(self, x):
        if self.anchor == "left":
            return 0 if x < 0 else x
        return 0 if x > Window.width else Window.width - x

    def on_touch_down(self, touch):
        if self.status == "closed":
            return False
        elif self.status == "opened":
            for child in self.children[:]:
                if child.dispatch("on_touch_down", touch):
                    return True
        return True

    def on_touch_move(self, touch):
        if self.status == "closed":
            if (
                self.get_dist_from_side(touch.ox) <= self.swipe_edge_width
                and abs(touch.x - touch.ox) > self.swipe_distance
            ):
                self.status = "opening_with_swipe"
        elif self.status == "opened":
            self.status = "closing_with_swipe"

        if self.status in ("opening_with_swipe", "closing_with_swipe"):
            self.open_progress = max(
                min(self.open_progress + touch.dx / self.width, 1), 0
            )
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.status == "opening_with_swipe":
            if self.open_progress > 0.5:
                self.set_state("open", animation=True)
            else:
                self.set_state("close", animation=True)
        elif self.status == "closing_with_swipe":
            if self.open_progress < 0.5:
                self.set_state("close", animation=True)
            else:
                self.set_state("open", animation=True)
        elif self.status == "opened":
            if (
                self.close_on_click
                and self.get_dist_from_side(touch.ox) > self.width
            ):
                self.set_state("close", animation=True)
        elif self.status == "closed":
            return False
        return True

    def _handle_keyboard(self, window, key, *largs):
        if key == 27 and self.status == "opened" and self.close_on_click:
            self.set_state("close")
            return True

if __name__ == "__main__":
    class Login(Screen):
        pass

    class Home(Screen):
        pass

    class Account(Screen):
        pass

    class NavigatorApp(MDApp):
        def build(self):
            return Builder.load_string("""
# NavigationContainer:

# StackNavigator:
#     Screen:
#         name: "screen1"
#         FlexLayout:
#             FlexButton:
#                 text: "go to screen2"
#                 on_release:
#                     root.current = "screen2"
#             FlexButton:
#                 text: "change title"
#                 on_release:
#                     root.title = "HELLO WORLD"
#     Screen:
#         name: "screen2"
#         FlexLayout:
#             FlexButton:
#                 text: "go to screen1"
#                 on_release:
#                     root.current = "screen1"

BottomNavigator:
    Login:
        name: "login"
        FlexLayout:
            FlexButton:
                text: "go to home"
                on_release:
                    root.current = "home"
    Home:
        name: "home"
        FlexLayout:
            FlexButton:
                text: "go to login"
                on_release:
                    root.current = "login"

NavigationLayout:
    ScreenManager:
        Screen:
            BoxLayout:
                orientation: 'vertical'
                MDToolbar:
                    title: "Navigation Drawer"
                    elevation: 10
                    left_action_items: [['menu', lambda x: nav_drawer.set_state()]]
                Widget:
    MDNavigationDrawer:
        id: nav_drawer
        BoxLayout:
            Button:
                text: "hello world"
""")

    NavigatorApp().run()