from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from django.conf import settings


class AppRegisterException(Exception):
    pass


class ImproperlyConfigured(Exception):
    pass


class InvalidOperation(AppRegisterException):
    pass


class AlreadyRegistered(AppRegisterException):
    pass


class NotRegistered(AppRegisterException):
    pass


class BaseRegistry(object):

    def __init__(self):
        self._registry = set()

    def all(self):
        return self._registry

    def autodiscover(self):

        for app in settings.INSTALLED_APPS:
            try:
                import_module(".registry", app)
            except ImportError:
                if module_has_submodule(import_module(app), "fixture_gen"):
                    raise
                continue


class Registry(BaseRegistry):

    def register(self, obj):

        if not issubclass(obj, self.base):
            raise InvalidOperation("Object '%s' is not a '%s'" % (obj, self.base))

        if obj in self._registry:
            raise AlreadyRegistered("Object '%s' has already been registered" % obj)

        self._registry.add(obj)

    def unregister(self, obj):

        self._registry.remove(obj)
