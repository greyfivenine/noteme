from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Note
from django.utils import timezone

class UserForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class NoteForm(forms.ModelForm):
    group_name = forms.CharField(widget=forms.TextInput(), max_length=50, empty_value='Нет группы')
    class Meta:
        model = Note
        fields = ('text', 'planned_date')

    def clean_planned_date(self):
        planned_date = self.cleaned_data['planned_date']

        if planned_date < timezone.now():
            raise ValidationError('Дата не может быть меньше текущей')
        else:
            return planned_date
