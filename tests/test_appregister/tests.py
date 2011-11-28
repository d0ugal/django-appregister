from django.utils import unittest
import sys


class RegistryProcessTestCase(unittest.TestCase):

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

    @unittest.skipIf(sys.version_info < (2, 6),
                     "Class decorators now supported in earlier than Python 2.6")
    def test_decorator_register(self):
        """
        Test trying registering a class with a decorator.
        """

        from test_appregister.models import Question, registry

        @registry.register
        class MyQuestion(Question):
            pass

        self.assertIn(MyQuestion, registry.all())

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


class NamedRegistryTestCase(unittest.TestCase):

    def test_basic_registry(self):

        from appregister import NamedRegistry
        from appregister.base import InvalidOperation, AlreadyRegistered
        from test_appregister.models import Question

        class MyRegistry(NamedRegistry):
            base = Question

        registry = MyRegistry()

        # Test the registry allows a valid registration and block an invalid.
        class MyTestSubClass(Question):
            pass

        registry.register('first', MyTestSubClass)

        with self.assertRaises(AlreadyRegistered):
            registry.register('first', MyTestSubClass)

        registry.register('second', MyTestSubClass)

        class MyObject(object):
            pass

        with self.assertRaises(InvalidOperation):
            registry.register('invalid', MyObject)

        registry.unregister('first')

        with self.assertRaises(KeyError):
            registry['first']

        self.assertEqual(registry['second'], MyTestSubClass)
        self.assertEqual(len(registry), 1)

        for i in registry:
            self.assertIn(i, registry.names())


class RegistryDefinitionTestCase(unittest.TestCase):

    def setUp(self):
        """
        Start with a clean registry for each test.
        """

        from test_appregister import models
        models.registry = models.QuestionRegistry()

    def test_basic_registry(self):

        from appregister import Registry
        from appregister.base import InvalidOperation
        from test_appregister.models import Question

        class MyRegistry(Registry):
            base = Question

        registry = MyRegistry()

        # Test the registry allows a valid registration and block an invalid.
        class MySubClass(Question):
            pass

        registry.register(MySubClass)

        class MyObject(object):
            pass

        with self.assertRaises(InvalidOperation):
            registry.register(MyObject)

    def test_dotted_path_base(self):
        """
        Test defining a base for the registry as a dotted path to avoid the
        circular import problem.
        """

        from appregister import Registry
        from appregister.base import InvalidOperation

        class MyRegistry(Registry):
            base = 'test_appregister.models.Question'

        registry = MyRegistry()

        from test_appregister.models import Question

        # Test the registry allows a valid registration and block an invalid.
        class MySubClass(Question):
            pass

        registry.register(MySubClass)

        class MyObject(object):
            pass

        with self.assertRaises(InvalidOperation):
            registry.register(MyObject)


class AutodiscoverTestCase(unittest.TestCase):

    def setUp(self):
        """
        Start with a clean registry for each test.
        """

        from test_appregister import models
        models.registry = models.QuestionRegistry()

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
