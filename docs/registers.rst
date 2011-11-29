Register Reference Guide
========================

Appregister comes with two different build in Registries, Register and
NamedRegister.


Register
----------------------------------------

The `Register` class is the simplest registry, for storing a set of unique
subclasses. A Register can be defined like so::

    from appregister import Register

    class QuestionRegister(Register):
        base = 'myproject.Question'
        discovermodule = 'questions'

    questions = QuestionRegister()

Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Register class implements the Sized and Iterable ABC's from the collections
module and adds the following methods.

``all``
    Accepts no arguements and returns a set containing all of the registered
    subclases.

``autodiscover``
    Accepts no arguements and checks each of the ``INSTALLED_APPS`` for a
    module with the same named as ``discovermodule`` to find any registered
    subclasses.

``clear``
    Accepts no arguements and resets the registry and removes any previously
    registered classes.

``regsiter``
    Accepts a class object that must extend ``base``. This class is added to
    the registry.

    The exception ``appregister.base.AlreadyRegistered`` is raised if the class
    has already been registered.

    The exception ``appregister.base.InvalidOperation`` is raised if the class
    is not a subclass of ``base``.

``unregister``
    Accepts a class, and removes it from the registry. If the class is not
    registered a ``KeyError`` is raised.

Usage Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example assumes that the QuestionRegister that is defined above
is added to the file ``registry.py`` in your myproject package::

    from myproject import registry

    @registry.questions.register
    class MultipleChoiceQuestion(Question):
        pass
        # ...

    # If you are using a Python version older than 2.6, rather than using the
    # function as a class based decorator you will nee to use

    Class MultipleChoiceQuestion(Question):
        pass
        # ...

    registry.questions.registered(MultipleChoiceQuestion)



NamedRegister
----------------------------------------

The named register includes all of the functionality of the Register class but
extended to require a name (or key) for each registered subclass. The
NamedRegister also doesn't require registered classes to be unique, other than
a key can only be registered once.

The ``NamedRegister`` does not require any further steps than ``Register`` when
defining your class register, so it can be defined like so::

    from appregister import NamedRegister

    class NamedQuestionRegister(NamedRegister):
        base = 'myproject.Question'
        discovermodule = 'questions'

    named_questions = NamedQuestionRegister()

Reference
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Register class implements the Mapping ABC from the collections module, so it
can be used like a dict and it also adds/changes the following methods.

``all``
    Accepts no arguements and returns a dict containing all of the registered
    subclases.

``regsiter``
    Accepts a key and a class object that must extend ``base``. This class is
    added to the registry under the given key.

    The exception ``appregister.base.AlreadyRegistered`` is raised if the key
    has already been registered.

    The exception ``appregister.base.InvalidOperation`` is raised if the class
    is not a subclass of ``base``.

``unregister``
    Accepts a key, and removes it from the registry. If the key is not
    registered a ``KeyError`` is raised.

``names``
    Accepts no arguements and returns a list of all the registered names.

Usage Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following example like with the Register example assumes that the
NamedQuestionRegister is added to the file ``registry.py`` in your
myproject package::

    from myproject import registry

    @registry.named_questions.register("Multiple Choice")
    class MultipleChoiceQuestion(Question):
        pass
        # ...

    # If you are using a Python version older than 2.6, rather than using the
    # function as a class based decorator you will nee to use

    Class MultipleChoiceQuestion(Question):
        pass
        # ...

    registry.questions.registered("Multiple Choice", MultipleChoiceQuestion)