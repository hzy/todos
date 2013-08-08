from django.test import TestCase

from .models import Todo, TodoList
from .views import TodoCompleteView

class TodoListModelTests(TestCase):
    def setUp(self):
        self.todolist = TodoList.objects.create(
            name='Test Todolist'
        )

    def test_get_absolute_url_works(self):
        url = self.todolist.get_absolute_url()
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

class TodoModelTests(TestCase):
    def setUp(self):
        self.todolist = TodoList.objects.create(
            name='Test Todolist'
        )
        self.todo = Todo.objects.create(
            label='Test Todo',
            list=self.todolist
        )

    def test_get_complete_url_works(self):
        url = self.todo.get_complete_url()

        resp = self.client.post(url)

        self.assertEqual(resp.status_code, 302)


class TodoManagerTests(TestCase):
    def setUp(self):
        self.todolist = TodoList.objects.create(
            name='Test Todolist'
        )
        for x in xrange(5):
            Todo.objects.create(
                label='Test Todo ' + str(x),
                list=self.todolist,
                is_done=False
            )
        for x in xrange(5):
            Todo.objects.create(
                label='Test Todo ' + str(x+5),
                list=self.todolist,
                is_done=True
            )

    def test_complete_queryset_method_only_returns_instances_with_is_done_true(self):
        qs = Todo.objects.complete()
        self.assertEqual(len(qs), 5)
        for todo in qs:
            self.assertTrue(todo.is_done)

    def test_incomplete_queryset_method_only_returns_instances_with_is_done_false(self):
        qs = Todo.objects.incomplete()
        self.assertEqual(len(qs), 5)
        for todo in qs:
            self.assertFalse(todo.is_done)

class TodoCompleteViewTests(TestCase):
    def setUp(self):
        self.todolist = TodoList.objects.create(
            name='Test Todolist'
        )
        self.todo = Todo.objects.create(
            label='Test Todo',
            list=self.todolist
        )
        self.view = TodoCompleteView()

    def test_view_sets_is_done_to_true_for_todo(self):
        self.assertFalse(self.todo.is_done)
        resp = self.client.post(self.todo.get_complete_url(), {})
        
        self.todo = Todo.objects.get(pk=self.todo.pk)
        self.assertTrue(self.todo.is_done)

    def test_get_todo_list_returns_todo_list_based_on_pk_in_kwargs(self):
        self.view.kwargs = {'pk': self.todolist.pk}
        result = self.view.get_todo_list()
        self.assertEqual(result, self.todolist)

    def test_get_todo_returns_todo_based_on_todo_pk_in_kwargs(self):
        self.view.kwargs = {'todo_pk': self.todo.pk}
        result = self.view.get_todo()
        self.assertEqual(result, self.todo)
