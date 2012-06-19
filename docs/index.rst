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

First, you should create your base class that all registered classes will be a
subclass of. Often this is a base Model class in your models.py but it can be
any python class anywhere in your project.

.. doctest::

    >>> class AppPlugin(object):
    ...     pass

You then need to declare your register. It only had one required property;
``base``. The base can either be a class object, or a dotted string to the
class, such as ``"myapp.AppPlugin"``.

The other most common property is the ``discovermodule`` property. This
provides a way to automatically discover subclasses within a project. You can
choose any name here that would make a valid Python package name and then
appregister will look through the ``INSTALLED_APPS`` in your Django settings
and find registered items. For example, if you use the discovermodule value
``plugins`` and have the app ``myblog`` in your installed apps, then app
register will look in ``myblog.plugins`` for registered classes.

.. doctest::

    >>> from appregister import SortedRegistry

    >>> class MyRegistry(SortedRegistry):
    ...     base = AppPlugin
    ...     discovermodule = 'plugins'

After that, you can go ahead and create an instance of the registry -
creating it at the module level makes it easy to re-use across the project
(but you can have as many instances as you need). It's good practice to
create your registry in its own module, such as ``myapp/register.py``.

.. doctest::

    >>> plugins = MyRegistry()

Now that we have the registry, if you want to use the autodiscover feature
you will need to add the following line in your base urls.py. Exactly like you
do for the Django admin. Import the registry instance from where you stored
it and then call autodiscover.

.. doctest::

    >>> plugins.autodiscover()

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
    <class 'MyPlugin'>
    <class 'MySecondPlugin'>

.. note::

    The order of registration is not stored. Since we can't tell what order they
    would be registered, if you want a sorted set you will need to sort them
    after they have all been registered.

.. doctest::

    >>> plugins.clear()
    >>> len(plugins)
    0