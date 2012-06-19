Changelog
=========

``v0.3.0`` (19/06/2012)
------------------------

* Greatly improved project layout and testing setup. Tests can now be run by
  using the command ``python setup.py test``.

* Added ``appregister.SortedRegister`` that behaves in a similar way to
  ``appregister.Register`` but preserves the order that items were added.

* Added hooks ``add_class`` and ``remove_class`` to ``appregister.Register``
  to make it easier to customise how classes are stored when using different
  (or custom) data storage.


``v0.2.0`` (07/12/2011)
------------------------

* Added a ``clear`` and a ``setup`` method to the registry to clarify the
  purpose when creating a new registry type subclass.


``v0.1.0`` (29/11/2011)
------------------------

Fixed a number of issues and improved documentation greatly.

* NamedRegisters can now be registered with class decorators with the style::

    @registry.register("Name")
    class SubClass(Base):
        pass

  The ``register`` method then, when only given a name returns a callable that
  accepts one arguement that is the class to be registered. This is already
  bound to the register and the name.

* Register now implements the Sized and Iterable ABC's from the collections
  module.

* NamedRegister implements the Mapping ABC from the collections module.

* Removed the ``names`` method on the NamedRegistry as it duplicates the
  ``keys`` method that is required by the Mapping ABC.
