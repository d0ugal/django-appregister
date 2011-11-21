from appregister.base import Registry

from test_appregister.models import Question


class QuestionRegistry(Registry):

    base = Question
    discovermodule = 'questions'


registry = QuestionRegistry()
