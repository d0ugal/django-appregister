from django.db import models


class BaseQuestion(models.Model):
    pass


class Question(BaseQuestion):
    pass

    class Meta:
        proxy = True


class BooleanQuestion(models.Model):
    pass
