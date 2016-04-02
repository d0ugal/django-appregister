Registry Reference Guide
========================

Appregister comes with a BaseRegistry and three built in implementations of
the registry; ``Registry``, ``NamedRegistry`` and ``SortedRegistry``. These
are similar but store the registered items in a noticibly different way. Each
of these will be discussed below.

.. testsetup:: *

    class Question(object):
        pass

.. module:: appregister.base

BaseRegistry
----------------------------------------

The base registry offers a common set of methods for creating a Registry system.
These hooks allow you to easily customise your Register works. There is a
noticable lack of three methods; setup, register and unregister as they are
specific to the type of registry system - examples below under ``Registry`` and
``NamedRegistry``.

.. autoclass:: BaseRegistry

    .. automethod:: setup
    .. automethod:: autodiscover
    .. automethod:: is_valid
    .. automethod:: is_registered
    .. automethod:: all
    .. automethod:: clear

.. module:: appregister

Registry
----------------------------------------

The `Registry` class is the simplest registry, for storing a set of unique
subclasses. A Registry can be defined like so

.. doctest::

    >>> from appregister import Registry

    >>> class QuestionRegistry(Registry):
    ...     base = Question
    ...     discovermodule = 'questions'

    >>> questions = QuestionRegistry()

Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: Registry

    .. automethod:: register
    .. automethod:: unregister
    .. automethod:: add_class
    .. automethod:: remove_class


Usage Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example assumes that the QuestionRegistry that is defined above
is added to the file ``registry.py`` in your myproject package.

.. doctest::

    >>> # re-initialise the Registry.
    >>> questions.setup()

    >>> questions.all()
    set([])

    >>> @questions.register
    ... class MultipleChoiceQuestion(Question):
    ...     pass

    >>> questions.all()
    set([<class 'MultipleChoiceQuestion'>])

    >>> # Trigger the autodiscover to find all the third party subclasses
    >>> questions.autodiscover()

    >>> questions.is_valid(MultipleChoiceQuestion)
    True
    >>> questions.is_valid(object)
    False
    >>> questions.is_registered(MultipleChoiceQuestion)
    True
    >>> questions.clear()
    >>> questions.is_registered(MultipleChoiceQuestion)
    False



NamedRegistry
----------------------------------------

The named register includes all of the functionality of the Registry class but
extended to require a name (or key) for each registered subclass. The
NamedRegistry also doesn't require registered classes to be unique, other than
a key can only be registered once.

The ``NamedRegistry`` does not require any further steps than ``Registry`` when
defining your class register, so it can be defined like so

.. doctest::

    >>> from appregister import NamedRegistry

    >>> class NamedQuestionRegistry(NamedRegistry):
    ...     base = Question
    ...     discovermodule = 'questions'

    >>> named_questions = NamedQuestionRegistry()

Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Registry class implements the Mapping ABC from the collections module, so it
can be used like a dict and it also adds/changes the following methods.

.. autoclass:: NamedRegistry

    .. automethod:: register
    .. automethod:: unregister


Usage Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example like with the Registry example assumes that the
NamedQuestionRegistry is added to the file ``registry.py`` in your
myproject package

.. doctest::

    >>> # re-initialise the Registry.
    >>> named_questions.setup()

    >>> named_questions.all()
    {}

    >>> @named_questions.register("Multiple Choice")
    ... class MultipleChoiceQuestion(Question):
    ...     pass

    >>> named_questions.all()
    {'Multiple Choice': <class 'MultipleChoiceQuestion'>}

    >>> # Trigger the autodiscover to find all the third party subclasses
    >>> named_questions.autodiscover()

    >>> named_questions.is_valid(MultipleChoiceQuestion)
    True
    >>> named_questions.is_valid(object)
    False
    >>> named_questions.is_registered("Multiple Choice")
    True
    >>> named_questions.clear()
    >>> named_questions.is_registered("Multiple Choice")
    False


SortedRegistry
----------------------------------------

The `SortedRegistry` class is a simple extension on the base ``Registry``
that persists the order which classes are registered.

.. doctest::

    >>> from appregister import SortedRegistry

    >>> class SortedQuestionRegistry(SortedRegistry):
    ...     base = Question
    ...     discovermodule = 'questions'

    >>> questions = SortedQuestionRegistry()

Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: SortedRegistry

    .. automethod:: register
    .. automethod:: unregister


Usage Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example assumes that the QuestionRegistry that is defined above
is added to the file ``registry.py`` in your myproject package.

.. doctest::

    >>> # re-initialise the Registry.
    >>> questions.setup()

    >>> questions.all()
    []

    >>> @questions.register
    ... class MultipleChoiceQuestion(Question):
    ...     pass

    >>> @questions.register
    ... class BooleanQuestion(Question):
    ...     pass

    >>> questions.all()
    [<class 'MultipleChoiceQuestion'>, <class 'BooleanQuestion'>]

    >>> # Trigger the autodiscover to find all the third party subclasses
    >>> questions.autodiscover()

    >>> questions.is_valid(MultipleChoiceQuestion)
    True
    >>> questions.is_valid(object)
    False
    >>> questions.is_registered(MultipleChoiceQuestion)
    True
    >>> questions.clear()
    >>> questions.is_registered(MultipleChoiceQuestion)
    False
