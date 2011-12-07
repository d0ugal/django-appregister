Django appregister
========================================

Django appregister is a building blocks app to implement a class registry
system for your django app. It uses a similar approach to the Django admin,
allowing you to register classes and supports an autodiscover feature.

A register based system provides a good base for making an app plugable and
extendable by third parties as they can register their own subclasses and your
code is able to use them.


Contents
========

.. toctree::
 :maxdepth: 1

 registers
 changelog

Installation
========================================

Use pip::

    pip install django-appregister


Quick Example Usage
========================================

First, you should create your base class that all registered classes must be a
subclass of. Often this is a base Model class in your models.py or it can be
anywhere in your project.

.. doctest::

    >>> class AppPlugin(object):
    ...     pass

Then you need to create your own registry, the base can either be a class, or a
dotted string that points to the base class, such as ``"myapp.AppPlugin"``.
After that, you can go ahead and create an instance of the registry - creating
it at the module level makes it easy to re-use across the project but you can
have as many instances as you need. It's good practice to create your registry
in its own module, such as ``myapp/register.py``.

.. doctest::

    >>> from appregister import Registry

    >>> class MyRegistry(Registry):
    ...     base = AppPlugin
    ...     discovermodule = 'plugins'

    >>> plugins = MyRegistry()

Now that you have the registry, you can start to add subclasses to it. This can
be done by using the class decorator on your register.

.. doctest::

    >>> @plugins.register
    ... class MyPlugin(AppPlugin):
    ...     pass

.. note::

    If you are using version 2.5 or below of Python you can't use the class
    based decorator, you will need to call it manually. The above example would
    then become;

    .. doctest::

        >>> class MySecondPlugin(AppPlugin):
        ...     pass
        >>> plugins.register(MySecondPlugin)
        <class 'MySecondPlugin'>

Registering an invalid object will raise an InvalidOperation exception

.. doctest::

    >>> # Note that this class does not inherit from the base we specified.
    >>> class MyNonSubclass(object):
    ...     pass

    >>> plugins.register(MyNonSubclass)
    Traceback (most recent call last):
        ...
    InvalidOperation: Object 'MyNonSubclass' is not a subclass of 'AppPlugin'

Finally, now you can get all your objects back - this includes those registered
by a third party.

.. doctest::

    >>> len(plugins)
    2

    >>> for plugin in plugins:
    ...     print plugin
    <class 'MySecondPlugin'>
    <class 'MyPlugin'>

.. note::

    The order of registration is not stored. Since we can't tell what order they
    would be registered, if you want a sorted set you will need to sort them
    after they have all been registered.

.. doctest::

    >>> plugins.clear()
    >>> len(plugins)
    0

.. automodule:: appregister
   :members:
