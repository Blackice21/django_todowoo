from django.forms import ModelForm
from .models import todos

class Todoform(ModelForm):
    class Meta:
        model = todos
        fields = ['title', 'memo', 'important']