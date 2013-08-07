from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User


class TodoList(models.Model):
    name = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('todolist_detail', args=(self.pk,))


class Todo(models.Model):
    label = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    list = models.ForeignKey(TodoList)

