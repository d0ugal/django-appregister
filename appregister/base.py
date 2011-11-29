from collections import Mapping, Sized, Iterable

from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from django.core.urlresolvers import get_callable
from django.conf import settings


class AppRegisterException(Exception):
    "Base exception for catching an errors raised directly by Appregister"


class InvalidOperation(AppRegisterException):
    """
    Raised when attempting to register a invalid class or object. This would be
    if either the object is not a class, or the class does not subclass the
    base.
    """


class AlreadyRegistered(AppRegisterException):
    """
    Raised when trying to register a class that is already registered.
    """


class BaseRegistry(Sized, Iterable):

    def __init__(self):
        """
        Initialise the datastore for the register and determine if the provided
        base is a dotted path or already an object.
        """

        self.setup()

        if not callable(self.base):
            self.base_str = self.base
            self.base = None

    def __iter__(self):
        return iter(self._registry)

    def __len__(self):
        return len(self._registry)

    def get_bases(self):
        """
        Get the base class from the dotted path, or return the base class if it
        has already been determined.
        """
        if self.base is not None:
            return self.base

        self.base = get_callable(self.base_str)
        return self.base

    def all(self):
        """
        Return the register data structure.
        """
        return self._registry

    def autodiscover(self, module=None):
        """
        Import ``module`` from each of the INSTALLED_APPS defined in the
        settings to find any registered classes.
        """

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
        """
        Returns True if the class is valid for this register, otherwise False
        is returned.
        """
        return issubclass(class_, self.get_bases())

    def is_registered(self, class_):
        """
        Return True is the class is already registered. Otherwise return False
        """
        return class_ in self._registry

    def setup(self):
        """
        Initialise the registry data structure.
        """
        self._registry = set()

    def clear(self):
        """
        Reset the registry by remvoing all items/re-creating the data structure.
        """
        self.setup()


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


class NamedRegistry(BaseRegistry, Mapping):

    def setup(self):
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
