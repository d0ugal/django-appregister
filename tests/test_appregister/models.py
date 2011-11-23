from django.db import models
from appregister.base import Registry


class BaseQuestion(models.Model):

    class Meta:
        proxy = True


class BooleanQuestion(BaseQuestion):
    pass


class MultipleChoiceQuestion(BaseQuestion):
    pass


# Setting up the registry.


class QuestionRegistry(Registry):

    base = BaseQuestion
    discovermodule = 'questions'

registry = QuestionRegistry()
registry.register(BooleanQuestion)
registry.register(MultipleChoiceQuestion)
