Django appregister
========================================

Django appregister is a building blocks app to implement a registry system for
your django app. It uses a similar approach to the Django admin, allowing you
to register classes and supports an autodiscover feature.

A register based system provides a good base for making an app plugable and
extendable by third parties as they can register their own subclasses and your
code is able to use them.


Installation
========================================

Use pip::

    pip install django-appregister


Quick Example Usage
========================================

First, you should create your base class that all registede classes must be a
subclass of::

    # in models.py
    class AppPlugin(object):
        pass

Then you need to create your own registry, the base can either be a class, or a
dotted string that points to the base path, such as ``"myproject.AppPlugin"``.
After that, you can go ahead and create an instance of the registry - creating
it at the module level makes it easy to re-use across the project but you can
have as many instances as you need::

    # in registry.py
    from appregister import Registry

    class MyRegistry(Registry):
        base = 'myprojct.models.AppPlugin'
        discovermodule = ''

    plugins = MyRegistry()

Now that you have the registry, you can start to add subclasses to it::

    # in models.py

    from myproject import registry

    class MyPlugin(AppPlugin):
        pass

    registry.plugins.register(MySubclass)

Registering an invalid object will raise an InvalidOperation exception::

    # Note that this class does not inherit from the base we specified.
    class MyNonSubclass(object):
        pass

    registry.plugins.register(MyNonSubclass)

Finally, now you can get all your objects back - this includes those registered
by a third party.

    classes = registry.all()

Contents
========

.. toctree::
 :maxdepth: 1

 registers
 changelog