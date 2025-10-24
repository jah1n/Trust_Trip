from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Driver


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

