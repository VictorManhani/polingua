__all__ = ('FlexApp', 'runTouchApp', 'async_runTouchApp', 'stopTouchApp')

import os
from inspect import getfile
from os.path import dirname, join, exists, sep, expanduser, isfile
from kivy.config import ConfigParser
from kivy.base import runTouchApp, async_runTouchApp, stopTouchApp
from kivy.compat import string_types
from kivy_modules.factory import FlexFactory
from kivy.logger import Logger
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.resources import resource_find
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from kivy.setupconfig import USE_SDL2


class FlexApp(EventDispatcher):
    title = StringProperty(None)
    icon = StringProperty(None)
    use_kivy_settings = True
    settings_cls = ObjectProperty(None)
    kv_directory = StringProperty(None)
    kv_file = StringProperty(None)

    # Return the current running FlexApp instance
    _running_app = None

    __events__ = ('on_start', 'on_stop', 'on_pause', 'on_resume',
                  'on_config_change', )

    # Stored so that we only need to determine this once
    _user_data_dir = ""

    def __init__(self, **kwargs):
        FlexApp._running_app = self
        self._app_directory = None
        self._app_name = None
        self._app_settings = None
        self._app_window = None
        super(FlexApp, self).__init__(**kwargs)
        self.built = False

        #: Options passed to the __init__ of the FlexApp
        self.options = kwargs

        #: Returns an instance of the :class:`~kivy.config.ConfigParser` for
        #: the application configuration. You can use this to query some config
        #: tokens in the :meth:`build` method.
        self.config = None

        #: The *root* widget returned by the :meth:`build` method or by the
        #: :meth:`load_kv` method if the kv file contains a root widget.
        self.root = None

    def build(self):
        if not self.root:
            return Widget()

    def build_config(self, config):
        pass

    def build_settings(self, settings):
        pass

    def load_kv(self, filename=None):
        # Detect filename automatically if it was not specified.
        if filename:
            filename = resource_find(filename)
        else:
            try:
                default_kv_directory = dirname(getfile(self.__class__))
                if default_kv_directory == '':
                    default_kv_directory = '.'
            except TypeError:
                # if it's a builtin module.. use the current dir.
                default_kv_directory = '.'

            kv_directory = self.kv_directory or default_kv_directory
            clsname = self.__class__.__name__.lower()
            if (clsname.endswith('app') and
                    not isfile(join(kv_directory, '%s.kv' % clsname))):
                clsname = clsname[:-3]
            filename = join(kv_directory, '%s.kv' % clsname)

        # Load KV file
        Logger.debug('FlexApp: Loading kv <{0}>'.format(filename))
        rfilename = resource_find(filename)
        if rfilename is None or not exists(rfilename):
            Logger.debug('FlexApp: kv <%s> not found' % filename)
            return False
        root = Builder.load_file(rfilename)
        if root:
            self.root = root
        return True

    def get_application_name(self):
        if self.title is not None:
            return self.title
        clsname = self.__class__.__name__
        if clsname.endswith('FlexApp'):
            clsname = clsname[:-3]
        return clsname

    def get_application_icon(self):
        if not resource_find(self.icon):
            return ''
        else:
            return resource_find(self.icon)

    def get_application_config(self, defaultpath='%(appdir)s/%(appname)s.ini'):
        if platform == 'android':
            return join(self.user_data_dir, '.{0}.ini'.format(self.name))
        elif platform == 'ios':
            defaultpath = '~/Documents/.%(appname)s.ini'
        elif platform == 'win':
            defaultpath = defaultpath.replace('/', sep)
        return expanduser(defaultpath) % {
            'appname': self.name, 'appdir': self.directory}

    @property
    def root_window(self):
        return self._app_window

    def load_config(self):
        try:
            config = ConfigParser.get_configparser('app')
        except KeyError:
            config = None
        if config is None:
            config = ConfigParser(name='app')
        self.config = config
        self.build_config(config)
        # if no sections are created, that's mean the user don't have
        # configuration.
        if len(config.sections()) == 0:
            return
        # ok, the user have some sections, read the default file if exist
        # or write it !
        filename = self.get_application_config()
        if filename is None:
            return config
        Logger.debug('FlexApp: Loading configuration <{0}>'.format(filename))
        if exists(filename):
            try:
                config.read(filename)
            except:
                Logger.error('FlexApp: Corrupted config file, ignored.')
                config.name = ''
                try:
                    config = ConfigParser.get_configparser('app')
                except KeyError:
                    config = None
                if config is None:
                    config = ConfigParser(name='app')
                self.config = config
                self.build_config(config)
                pass
        else:
            Logger.debug('FlexApp: First configuration, create <{0}>'.format(
                filename))
            config.filename = filename
            config.write()
        return config

    @property
    def directory(self):
        if self._app_directory is None:
            try:
                self._app_directory = dirname(getfile(self.__class__))
                if self._app_directory == '':
                    self._app_directory = '.'
            except TypeError:
                # if it's a builtin module.. use the current dir.
                self._app_directory = '.'
        return self._app_directory

    def _get_user_data_dir(self):
        # Determine and return the user_data_dir.
        data_dir = ""
        if platform == 'ios':
            data_dir = expanduser(join('~/Documents', self.name))
        elif platform == 'android':
            from jnius import autoclass, cast
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            context = cast('android.content.Context', PythonActivity.mActivity)
            file_p = cast('java.io.File', context.getFilesDir())
            data_dir = file_p.getAbsolutePath()
        elif platform == 'win':
            data_dir = os.path.join(os.environ['APPDATA'], self.name)
        elif platform == 'macosx':
            data_dir = '~/Library/Application Support/{}'.format(self.name)
            data_dir = expanduser(data_dir)
        else:  # _platform == 'linux' or anything else...:
            data_dir = os.environ.get('XDG_CONFIG_HOME', '~/.config')
            data_dir = expanduser(join(data_dir, self.name))
        if not exists(data_dir):
            os.mkdir(data_dir)
        return data_dir

    @property
    def user_data_dir(self):
        if self._user_data_dir == "":
            self._user_data_dir = self._get_user_data_dir()
        return self._user_data_dir

    @property
    def name(self):
        if self._app_name is None:
            clsname = self.__class__.__name__
            if clsname.endswith('FlexApp'):
                clsname = clsname[:-3]
            self._app_name = clsname.lower()
        return self._app_name

    def _run_prepare(self):
        if not self.built:
            self.load_config()
            self.load_kv(filename=self.kv_file)
            root = self.build()
            if root:
                self.root = root
        if self.root:
            if not isinstance(self.root, Widget):
                Logger.critical('FlexApp.root must be an _instance_ of Widget')
                raise Exception('Invalid instance in FlexApp.root')
            from kivy.core.window import Window
            Window.add_widget(self.root)

        # Check if the window is already created
        from kivy.base import EventLoop
        window = EventLoop.window
        if window:
            self._app_window = window
            window.set_title(self.get_application_name())
            icon = self.get_application_icon()
            if icon:
                window.set_icon(icon)
            self._install_settings_keys(window)
        else:
            Logger.critical("Application: No window is created."
                            " Terminating application run.")
            return

        self.dispatch('on_start')

    def run(self):
        self._run_prepare()
        runTouchApp()
        self.stop()

    async def async_run(self, async_lib=None):
        self._run_prepare()
        await async_runTouchApp(async_lib=async_lib)
        self.stop()

    def stop(self, *largs):
        self.dispatch('on_stop')
        stopTouchApp()

        # Clear the window children
        if self._app_window:
            for child in self._app_window.children:
                self._app_window.remove_widget(child)
        FlexApp._running_app = None

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    @staticmethod
    def get_running_app():
        return FlexApp._running_app

    def on_config_change(self, config, section, key, value):
        pass

    def open_settings(self, *largs):
        if self._app_settings is None:
            self._app_settings = self.create_settings()
        displayed = self.display_settings(self._app_settings)
        if displayed:
            return True
        return False

    def display_settings(self, settings):
        win = self._app_window
        if not win:
            raise Exception('No windows are set on the application, you cannot'
                            ' open settings yet.')
        if settings not in win.children:
            win.add_widget(settings)
            return True
        return False

    def close_settings(self, *largs):
        win = self._app_window
        settings = self._app_settings
        if win is None or settings is None:
            return
        if settings in win.children:
            win.remove_widget(settings)
            return True
        return False

    def create_settings(self):
        if self.settings_cls is None:
            from kivy.uix.settings import SettingsWithSpinner
            self.settings_cls = SettingsWithSpinner
        elif isinstance(self.settings_cls, string_types):
            self.settings_cls = FlexFactory.get(self.settings_cls)
        s = self.settings_cls()
        self.build_settings(s)
        if self.use_kivy_settings:
            s.add_kivy_panel()
        s.bind(on_close=self.close_settings,
               on_config_change=self._on_config_change)
        return s

    def destroy_settings(self):
        if self._app_settings is not None:
            self._app_settings = None

    #
    # privates
    #

    def _on_config_change(self, *largs):
        self.dispatch('on_config_change', *largs[1:])

    def _install_settings_keys(self, window):
        window.bind(on_keyboard=self._on_keyboard_settings)

    def _on_keyboard_settings(self, window, *largs):
        key = largs[0]
        setting_key = 282  # F1

        # android hack, if settings key is pygame K_MENU
        if platform == 'android' and not USE_SDL2:
            import pygame
            setting_key = pygame.K_MENU

        if key == setting_key:
            # toggle settings panel
            if not self.open_settings():
                self.close_settings()
            return True
        if key == 27:
            return self.close_settings()

    def on_title(self, instance, title):
        if self._app_window:
            self._app_window.set_title(title)

    def on_icon(self, instance, icon):
        if self._app_window:
            self._app_window.set_icon(self.get_application_icon())