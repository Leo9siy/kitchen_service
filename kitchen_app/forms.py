from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from kitchen_app.models import CookModel, DishModel, IngredientModel


class CookCreateForm(UserCreationForm):

    class Meta:
        model = CookModel
        fields = ('username', 'email', 'year_of_experience', 'password1', 'password2')


class DishSearchForm(forms.Form):
    dish_name = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder" : "Search by dish name"}
        )
    )


class DishCreateForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=IngredientModel.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta:
        model = DishModel
        fields = "__all__"
