from django.test import TestCase


class ResolverTestCase(TestCase):

    def setUp(self):
        """
        Start with a clean registry for each test.
        """

        from test_appregister import models
        models.registry = models.QuestionRegistry()

    def test_register(self):
        """
        Test simple registration of a sublcass
        """

        from test_appregister.models import Question, registry

        class MyQuestion(Question):
            pass

        registry.register(MyQuestion)

    def test_non_subclass_register(self):
        """
        Test trying to register a non-sublcass, which is not allowed
        """

        from appregister.base import InvalidOperation
        from test_appregister.models import registry

        class NonSubclass(object):
            pass

        with self.assertRaises(InvalidOperation):
            registry.register(NonSubclass)

    def test_already_registered(self):
        """
        Test attempting to register a subclass more than once.
        """

        from appregister.base import AlreadyRegistered
        from test_appregister.models import Question, registry

        class MyQuestion2(Question):
            pass

        registry.register(MyQuestion2)

        with self.assertRaises(AlreadyRegistered):
            registry.register(MyQuestion2)

    def test_unregister(self):
        """
        Test the unregister process by registering, unregistering and
        registering again
        """

        from test_appregister.models import Question, registry

        class MyQuestion3(Question):
            pass

        registry.register(MyQuestion3)
        self.assertIn(MyQuestion3, registry.all())

        registry.unregister(MyQuestion3)
        self.assertNotIn(MyQuestion3, registry.all())

        registry.register(MyQuestion3)
        self.assertIn(MyQuestion3, registry.all())

    def test_unregister_without_register(self):
        """
        Try to unregister a class that was never registered
        """

        from test_appregister.models import Question, registry

        class MyQuestion4(Question):
            pass

        with self.assertRaises(KeyError):
            registry.unregister(MyQuestion4)

    def test_autodiscover(self):
        """
        Test a basic autodiscover to find all the registered items in each
        Django app
        """

        from test_appregister.models import registry

        registry.autodiscover()

        names = [(c.__module__, c.__name__) for c in registry.all()]
        self.assertIn(('test_appregister.questions', 'MyAutoDiscoveredQuestion'), names)

    def test_autodiscover_overwrite(self):
        """
        Test autodiscover with an overwrite of the module name
        """

        from test_appregister.models import registry

        registry.autodiscover('questions2')

        names = [(c.__module__, c.__name__) for c in registry.all()]
        self.assertIn(('test_appregister.questions2', 'MyAutoDiscoveredQuestion2'), names)

    def test_autodiscover_import_error(self):
        """
        Test autodiscover with a module that raises an import error. This is to
        test that the ImportError isn't masked by being misinterpreted as the
        question_error module not existing.
        """

        from test_appregister.models import registry

        with self.assertRaises(ImportError):
            registry.autodiscover('questions_error')

    def test_doesnt_contain_base(self):
        """
        Test the base class isn't registered.
        """

        from test_appregister.models import Question, registry

        self.assertEqual(registry.all(), set())

        class MyQuestion3(Question):
            pass

        registry.register(MyQuestion3)

        self.assertEqual(registry.all(), set([MyQuestion3, ]))
