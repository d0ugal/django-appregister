test:
	coverage run --branch --source=appregister `which django-admin.py` test --settings=tests.settings appregister
	coverage report