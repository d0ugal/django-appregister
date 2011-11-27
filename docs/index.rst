Django appregister
========================================

Django appregister is a building blocks app to implement a registry system for
your django app. It uses a similar approach to the Django admin, allowing you
to register classes and supports an autodiscover feature to find classes that
follow a naming convention within your app (in the same way that putting
ModelAdmin sublcassic in an admin.py is a convention.)

Installation
========================================

Use pip::

    pip install django-appregister


Example Usage
========================================

First, you need a base object for the registry to build from::

    class MyBase(object):
        pass

Then lets define your registry::

    from appregister import Registry

    class MyRegistry(Registry):
        base MyBase

    registry = MyRegistry()

Now you can register sub classes of your base model::

    class MySubclass(MyBase):
        pass

    registry.register(MySubclass)

Registering invalid object will raise an error::

    class MyNonSubclass(MyBase):
        pass

    registry.register(MyNonSubclass)

Finally, not you can get all your objects back - this includes those registered
by a third party.

    classes = registry.all()

Contents
========

.. toctree::
 :maxdepth: 1

 changelog