from django import forms

class TodoForm(forms.Form):
    label = forms.CharField(max_length=255)
