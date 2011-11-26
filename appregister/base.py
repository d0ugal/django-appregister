from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from django.core.urlresolvers import get_callable
from django.conf import settings


class AppRegisterException(Exception):
    pass


class ImproperlyConfigured(Exception):
    pass


class InvalidOperation(AppRegisterException):
    pass


class AlreadyRegistered(AppRegisterException):
    pass


class ClassDoesNotExist(AppRegisterException):
    pass


class BaseRegistry(object):

    def __init__(self):
        self.clear()

        if not callable(self.base):
            self.base_str = self.base
            self.base = None

    def get_bases(self):
        if self.base is not None:
            return self.base

        self.base = get_callable(self.base_str)
        return self.base

    def get_class(self, class_):
        return get_callable(class_)

    def all(self):
        return self._registry

    def autodiscover(self, module=None):

        if not module:
            module = self.discovermodule

        for app in settings.INSTALLED_APPS:
            try:
                import_module(".%s" % module, app)
            except ImportError:
                if module_has_submodule(import_module(app), module):
                    raise
                continue

    def is_valid(self, class_):
        return issubclass(class_, self.get_bases())

    def is_registered(self, class_):
        return class_ in self._registry

    def clear(self):
        self._registry = set()


class Registry(BaseRegistry):

    def register(self, class_):

        if not self.is_valid(class_):
            raise InvalidOperation("Object '%s' is not a '%s'" % (class_, self.base))

        if self.is_registered(class_):
            raise AlreadyRegistered("Object '%s' has already been registered" % class_)

        self._registry.add(class_)

        # Return the original class to allow this method to be used as a
        # class based decorator.
        return class_

    def unregister(self, obj):

        self._registry.remove(obj)


class NamedRegistry(Registry):

    def __init__(self):
        self.clear()

    def clear(self):
        self._registry = dict()

    def register(self, name, class_):

        if not self.is_valid(class_):
            raise InvalidOperation("Object '%s' is not a '%s'" % (class_, self.base))

        if self.is_registered(name):
            raise AlreadyRegistered("Object '%s' has already been registered" % class_)

        self._registry[name] = class_

    def unregister(self, name):
        self._registry.pop(name)
