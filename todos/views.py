from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, FormView, View

from .models import Todo, TodoList
from .forms import TodoForm

class TodoListListView(ListView):
    model = TodoList
    template_name = 'todos/todolist_list.html'


class TodoListDetailView(DetailView):
    model = TodoList
    template_name = 'todos/todolist_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TodoListDetailView, self).get_context_data(*args, **kwargs)
        context.update({'todo_form': TodoForm()})
        return context

class TodoCreateView(FormView):
    form_class = TodoForm
    
    def form_valid(self, form):
        todo_list = TodoList.objects.get(pk=self.kwargs['pk'])
        todo = Todo.objects.create(
            label=form.cleaned_data['label'],
            list=todo_list
        )
        return redirect(todo_list.get_absolute_url())

class TodoCompleteView(View):
    def get_todo_list(self):
        return TodoList.objects.get(pk=self.kwargs['pk'])

    def get_todo(self):
        return Todo.objects.get(pk=self.kwargs['todo_pk'])

    def post(self, *args, **kwargs):
        todo_list = self.get_todo_list()
        todo = self.get_todo()

        todo.is_done = True
        todo.save()

        return redirect(todo_list.get_absolute_url())
