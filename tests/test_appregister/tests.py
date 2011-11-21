from django.test import TestCase


class ResolverTestCase(TestCase):

    def test_api(self):

        from appregister.base import InvalidOperation, AlreadyRegistered
        from test_appregister.models import Question
        from test_appregister.registry import registry

        class MyQuestion(Question):
            pass

        registry.register(MyQuestion)

        class NonSubclass(object):
            pass

        with self.assertRaises(InvalidOperation):
            registry.register(NonSubclass)

        with self.assertRaises(AlreadyRegistered):
            registry.register(MyQuestion)
