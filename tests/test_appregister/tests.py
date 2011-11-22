from django.test import TestCase


class ResolverTestCase(TestCase):

    def test_api(self):

        from appregister.base import InvalidOperation, AlreadyRegistered
        from test_appregister.models import Question, registry

        class MyQuestion(Question):
            pass

        registry.register(MyQuestion)

        class NonSubclass(object):
            pass

        with self.assertRaises(InvalidOperation):
            registry.register(NonSubclass)

        with self.assertRaises(AlreadyRegistered):
            registry.register(MyQuestion)

    def test_auto_api(self):

        from appregister.base import InvalidOperation, AlreadyRegistered
        from test_appregister.models import Object, object_registry

        with self.assertRaises(InvalidOperation):
            class InvalidQuestion(object_registry.mixin()):
                pass

        class ValidSub(Object):
            pass

        with self.assertRaises(AlreadyRegistered):

            # It's auto registered, so this should fail.
            object_registry.register(ValidSub)
