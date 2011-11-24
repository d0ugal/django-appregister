from test_appregister.models import Question, registry


class MyAutoDiscoveredQuestion(Question):
    pass

registry.register(MyAutoDiscoveredQuestion)
