from django.conf.urls.defaults import patterns, url

from test_appregister.registry import questions
questions.autodiscover()

urlpatterns = patterns('test_appregsiter.views',
    url(r'^$', 'test_view'),
)
