from test_appregister.models import Question, registry


class MyAutoDiscoveredQuestion2(Question):
    pass

registry.register(MyAutoDiscoveredQuestion2)
