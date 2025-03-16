from django.contrib.auth.forms import UserCreationForm
from django.forms import forms

from kitchen_app.models import CookModel


class CookCreateForm(UserCreationForm):

    class Meta:
        model = CookModel
        fields = ('username', 'email', 'year_of_experience', 'password1', 'password2')

