from django.db import models
from django.db.models.query import QuerySet

class TodoQuerySet(QuerySet):
    def incomplete(self):
        return self.filter(is_done=False)

    def complete(self):
        return self.filter(is_done=True)

class TodoManager(models.Manager):
    def get_query_set(self):
        return TodoQuerySet(self.model)

    def __getattr__(self, attr, *args):
        # see https://code.djangoproject.com/ticket/15062 for details
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_query_set(), attr, *args)
