from django.db import models
from appregister.base import Registry, AutoRegistery


class BaseQuestion(models.Model):
    pass


class QuestionRegistry(Registry):

    base = BaseQuestion
    discovermodule = 'questions'


registry = QuestionRegistry()


class Question(BaseQuestion):
    pass

    class Meta:
        proxy = True


class BooleanQuestion(BaseQuestion):
    pass


class MultipleChoiceQuestion(BaseQuestion):
    pass

registry.register(BooleanQuestion)
registry.register(MultipleChoiceQuestion)


# Example 2

class BaseObject(object):
    pass


class ObjectRegistry(AutoRegistery):

    base = BaseObject
    discovermodule = 'objects'

object_registry = ObjectRegistry()


class Object(BaseObject, object_registry.mixin()):

    class Meta:
        proxy = True


class SubObject1(Object):
    pass


class SubObject2(Object):
    pass
