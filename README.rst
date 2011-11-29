Django Appregister
========================================

Django Appregister is a class registry system to allow you to easily implement
a puggable

See http://appregister.readthedocs.org/ for further documentation.


Usage Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``myapp/registry.py``::

    from appregister import Register

    class QuestionRegister(Register):
        base = 'myapp.models.Question'
        discovermodule = 'questions'

    questions = QuestionRegister()


if ``myapp/models.py``::

    from django.db import models
    from myapp import registry

    class Question(models.Model):
        pass

    @registry.questions.register
    class MultipleChoiceQuestion(Question):
        pass


You can then access all classes that have been registered by your app or by
another app that extends it::

    from myapp import registry

    classes = registry.questions.all()

If you add the following lines to your urls.py, you can autodiscover all
question sublclasses that have been added to any of the apps in your
INSTALLED_APPS::

    from myapp import registry

    registry.questions.autodiscover()

This then allows developers to add their own subclasses to ``questions.py``
within their apps and have them registered to the system for use, in a similar
way to the addition and registration of ModelAdmins in ``admin.py`` files for
Django's admin.