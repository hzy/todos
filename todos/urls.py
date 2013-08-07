from django.conf.urls import patterns, include, url

from .views import TodoListListView, TodoListDetailView, TodoCreateView

urlpatterns = patterns('',
    url(r'^$', TodoListListView.as_view(), name='todolist_list'),
    url(r'^(?P<pk>\d+)/$', TodoListDetailView.as_view(), name='todolist_detail'),
    url(r'^(?P<pk>\d+)/create/$', TodoCreateView.as_view(), name='todo_create'),
)
