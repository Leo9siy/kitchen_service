from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from kitchen_app.models import CookModel, DishModel, IngredientModel


class CookCreateForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    year_of_experience = forms.IntegerField()

    def clean_year_of_experience(self):
        year_of_experience = self.cleaned_data["year_of_experience"]
        if year_of_experience < 0 or year_of_experience > 100:
            raise forms.ValidationError("Enter a valid year of experience")
        return year_of_experience

    class Meta:
        model = CookModel
        fields = (
            "username", "email",
            "year_of_experience",
            "password1", "password2"
        )


class DishSearchForm(forms.Form):
    dish_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "Search by dish name"}
        ),
    )


class CookSearchForm(forms.Form):
    cook_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name"}
        ),
    )


class DishTypeSearchForm(forms.Form):
    type_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "Search by type"}
        ),
    )


class IngredientSearchForm(forms.Form):
    ingredient_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "Search by ingredient"}
        ),
    )


class DishCreateForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    ingredients = forms.ModelMultipleChoiceField(
        queryset=IngredientModel.objects,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = DishModel
        fields = "__all__"
