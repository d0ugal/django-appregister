from django.db import models
from appregister.base import Registry


class Question(models.Model):
    pass


class BooleanQuestion(Question):
    pass


class MultipleChoiceQuestion(Question):
    pass


# Setting up the registry.


class QuestionRegistry(Registry):

    base = Question
    discovermodule = 'questions'

registry = QuestionRegistry()
registry.register(BooleanQuestion)
registry.register(MultipleChoiceQuestion)
