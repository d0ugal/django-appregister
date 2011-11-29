Changelog
=========

``v0.1.0``
-----------

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

``v0.0.1``
-----------

Initial release with the main included features being
