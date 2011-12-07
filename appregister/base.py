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
            self.get_bases()

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
        Accepts no arguements and returns the datastructure that containins all
        of the registered subclases. The datastructure used should be defined in
        the subclasses ``setup`` method.
        """
        return self._registry

    def autodiscover(self, module=None):
        """
        Accepts either no arguements or the name of the module to check. It then
        looks at each of the ``INSTALLED_APPS`` for the given module name or
        with the same named as ``discovermodule`` to find any registered
        subclasses.
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
        Accepts one arguement which should be a class but can be any object and
        Returns True if the class is valid for this register. By default, it
        simply checks that ``class_`` is a subclass of ``base``.
        """
        return issubclass(class_, self.get_bases())

    def is_registered(self, class_):
        """
        Accepts one arguement which should be a class but can be any object and
        returns True if the object is registered already and False otherwise.
        By default it usess the ``in`` keyword to check if ``class`` is in
        ``self._registry``.
        """
        return class_ in self._registry

    def setup(self):
        """
        Initialise the registry data structure. This should set
        ``self._registry`` with the datastructure that will store registeed
        classes. This could be anything from a list to a dict or your own custom
        structure.
        """
        self._registry = set()

    def clear(self):
        """
        Accepts no arguements and resets the registry and removes any previously
        registered classes. By default this calls the ``setup`` method to
        re-initialise the register.
        """
        self.setup()


class Registry(BaseRegistry):
    """
    The Registry class is a simple register that accepts any subclass of the
    base to be registered once. It inherits from BaseRegistry and implements
    the Sized and Iterable ABC's from the collections module and adds the
    following methods.
    """

    def register(self, class_):
        """
        Accepts ``class_``, a class object that must extend ``base``. The
        class is added to the registry. the register method can be used as a
        regular method::

            registry.register(MyClass)

        Or as a class decorator::

            @registry.register
            class MyClass:
                pass

        The exception ``appregister.base.AlreadyRegistered`` is raised if the
        class has already been registered, as defined by the ``is_registered``
        method.

        The exception ``appregister.base.InvalidOperation`` is raised if the
        class is not a valid addition to this register, as defined by the
        ``is_valid`` method.
        """

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
        """
        Accepts ``class_``, a class object and removes it from the registry. If
        the class is not registered a ``KeyError`` is raised.
        """

        self._registry.remove(class_)


class NamedRegistry(BaseRegistry, Mapping):
    """
    The NamedRegistry class allows for classes to be registered with a ``name``
    (or key) that can be used to reference that class. Unlike ``Registry``, the
    ``NamedRegistry`` allows for classes to be registered multiple times, but
    a given name can only be used once. It inherits from BaseRegistry and also
    implements the Mapping ABC from the collections module
    """

    def setup(self):
        self._registry = dict()

    def register(self, name, class_=None):
        """
        Accepts a ``name`` and ``class_``, a class object that must extend
        ``base``. The class is added to the registry.::

            named_registry.register("My Class", MyClass)

        If no ``class_`` is provided. A class decorator (callable) is returned
        that is bound to the given ``name`` and accepts one arguement,
        ``_class``. This allows for the following use of the register method::

            @named_registry.register("My Class")
            class MyClass:
                pass

        The exception ``appregister.base.AlreadyRegistered`` is raised if the
        class has already been registered, as defined by the ``is_registered``
        method.

        The exception ``appregister.base.InvalidOperation`` is raised if the
        class is not a valid addition to this register, as defined by the
        ``is_valid`` method.
        """

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
        """
        Accepts a key, and removes it from the registry. If the key is not
        registered a ``KeyError`` is raised.
        """
        del self._registry[name]

    def __getitem__(self, key):
        return self._registry[key]
