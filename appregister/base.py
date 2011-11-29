from collections import Mapping, Sized, Iterable

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


class BaseRegistry(Sized, Iterable):

    def __init__(self):
        self.clear()

        if not callable(self.base):
            self.base_str = self.base
            self.base = None

    def __iter__(self):
        return iter(self._registry)

    def __len__(self):
        return len(self._registry)

    def get_bases(self):
        if self.base is not None:
            return self.base

        self.base = get_callable(self.base_str)
        return self.base

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
            msg = "Object '%s' is not a subclass of '%s'" % (class_.__name__,
                self.base.__name__)
            raise InvalidOperation(msg)

        if self.is_registered(class_):
            msg = "Object '%s' has already been registered" % class_.__name__
            raise AlreadyRegistered(msg)

        self._registry.add(class_)

        # Return the original class to allow this method to be used as a
        # class based decorator.
        return class_

    def unregister(self, class_):

        self._registry.remove(class_)


class NamedRegistry(Registry, Mapping):

    def __init__(self):
        self.clear()

    def clear(self):
        self._registry = dict()

    def register(self, name, class_=None):

        if self.is_registered(name):
            msg = "Object '%s' has already been registered" % class_.__name__
            raise AlreadyRegistered(msg)

        # If only name is provided, return a callable that accepts only the
        # class instance, this adds support for decorator registration on named
        # registries.
        if not class_:
            def inner(class_):
                return self.register(name, class_)
            return inner

        if not self.is_valid(class_):
            msg = "Object '%s' is not a subclass of '%s'" % (class_.__name__,
                self.base.__name__)
            raise InvalidOperation(msg)

        self._registry[name] = class_

        # Return the original class to allow this method to be used as a
        # class based decorator.
        return class_

    def unregister(self, name):
        del self._registry[name]

    def __getitem__(self, key):
        return self._registry[key]
