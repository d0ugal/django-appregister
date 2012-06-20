# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements/install.txt') as f:
    requirements = f.readlines()

with open('requirements/test.txt') as f:
    test_requirements = f.readlines()[1:] + requirements

setup(
    name="django-appregister",
    version=":versiontools:appregister:",
    url='http://appregsiter.readthedocs.org/',
    license=license,
    description="A Django app that provides the building blocks for an app registry system",
    long_description=readme,
    author='Dougal Matthews',
    author_email='dougal85@gmail.com',
    setup_requires=[
        'versiontools >= 1.6',
        'django'
    ],
    test_suite="runtests.runtests",
    tests_require=test_requirements,
    packages=find_packages(exclude=('tests', 'docs')),
    zip_safe=False,
    install_requires=requirements
)
