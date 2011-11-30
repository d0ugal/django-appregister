import os
import sys

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append("%s/.." % TEST_DIR)

COMPRESS_CACHE_BACKEND = 'locmem://'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'appregister',
    'test_appregister',
)

TEMPLATE_DIRS = (
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
)

ROOT_URLCONF = 'test_appregister.urls'

COVERAGE_ADDITIONAL_MODULES = ['appregister', ]
COVERAGE_CODE_EXCLUDES = []
COVERAGE_MODULE_EXCLUDES = []
