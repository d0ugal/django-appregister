# This file, on purpose, raises an ImportError. It is used in the tests to
# verify that ImportErrors are not lost (by mistaking the import error for this
# file not existing)

from fake_module_name import something
