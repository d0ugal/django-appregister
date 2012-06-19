# following PEP 386, versiontools will pick it up
__version__ = (0, 3, 0, "final", 0)

from appregister.base import Registry, NamedRegistry, SortedRegistry

__all__ = ['__version__', 'Registry', 'NamedRegistry', 'SortedRegistry']
