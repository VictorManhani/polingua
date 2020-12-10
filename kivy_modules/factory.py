__all__ = ('MFactory', 'FactoryBase', 'FactoryException')

import copy
from kivy.logger import Logger
from kivy.context import register_context


class FactoryException(Exception):
    pass


class FactoryBase(object):

    def __init__(self):
        super(FactoryBase, self).__init__()
        self.classes = {}

    @classmethod
    def create_from(cls, factory):
        obj = cls()
        obj.classes = copy.copy(factory.classes)
        return obj

    def is_template(self, classname):
        if classname in self.classes:
            return self.classes[classname]['is_template']
        else:
            return False

    def register(self, classname, cls=None, module=None, is_template=False,
                 baseclasses=None, filename=None, warn=False):
        if cls is None and module is None and baseclasses is None:
            raise ValueError(
                'You must specify either cls= or module= or baseclasses =')
        if classname in self.classes:
            if warn:
                info = self.classes[classname]
                Logger.warning('Factory: Ignored class "{}" re-declaration. '
                'Current -  module: {}, cls: {}, baseclass: {}, filename: {}. '
                'Ignored -  module: {}, cls: {}, baseclass: {}, filename: {}.'.
                format(classname, info['module'], info['cls'],
                       info['baseclasses'], info['filename'], module, cls,
                       baseclasses, filename))
            return
        self.classes[classname] = {
            'module': module,
            'cls': cls,
            'is_template': is_template,
            'baseclasses': baseclasses,
            'filename': filename}

    def unregister(self, *classnames):
        for classname in classnames:
            if classname in self.classes:
                self.classes.pop(classname)

    def unregister_from_filename(self, filename):
        to_remove = [x for x in self.classes
                     if self.classes[x]['filename'] == filename]
        for name in to_remove:
            del self.classes[name]

    def __getattr__(self, name):
        classes = self.classes
        if name not in classes:
            if name[0] == name[0].lower():
                # if trying to access attributes like checking for `bind`
                # then raise AttributeError
                raise AttributeError(
                    'First letter of class name <%s> is in lowercase' % name)
            raise FactoryException('Unknown class <%s>' % name)

        item = classes[name]
        cls = item['cls']

        # No class to return, import the module
        if cls is None:
            if item['module']:
                module = __import__(
                    name=item['module'],
                    fromlist='*',
                    level=0  # force absolute
                )
                if not hasattr(module, name):
                    raise FactoryException(
                        'No class named <%s> in module <%s>' % (
                            name, item['module']))
                cls = item['cls'] = getattr(module, name)

            elif item['baseclasses']:
                rootwidgets = []
                for basecls in item['baseclasses'].split('+'):
                    rootwidgets.append(Factory.get(basecls))
                cls = item['cls'] = type(str(name), tuple(rootwidgets), {})

            else:
                raise FactoryException('No information to create the class')

        return cls

    get = __getattr__

#: Factory instance to use for getting new classes
FlexFactory: FactoryBase = register_context('FlexFactory', FactoryBase)

# Now import the file with all registers
# automatically generated by build_factory
import kivy_modules.factory_registers  # NOQA
Logger.info('FlexFactory: %d symbols loaded' % len(FlexFactory.classes))

if __name__ == '__main__':
    from kivy_modules.app import FlexApp
    from kivy_modules.factory import FlexFactory

    class MainMApp(FlexApp):
        def build(self):
            return FlexFactory.FlexButton(text="hello world")
    
    MainMApp().run()