from pathlib import Path

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet
from django.templatetags import static

from kitchen_service.settings.base import STATIC_URL


class DishTypeModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class CookModel(AbstractUser):
    year_of_experience = models.IntegerField(default=0)
    username = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ["username"]

    def clean(self):
        if not(100 > self.year_of_experience >= 0):
            raise ValidationError("Please enter a valid year of experience")

    def __str__(self) -> str:
        return self.username


class IngredientModel(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class DishModel(models.Model):
    name = models.CharField(max_length=32, unique=True, null=False)
    description = models.TextField(max_length=200, blank=True, null=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)

    dish_type = models.ForeignKey(DishTypeModel, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(
        IngredientModel, related_name="dish_ingredients"
    )
    cooks = models.ManyToManyField(CookModel, related_name="dishes")

    class Meta:
        ordering = ["price"]

    def clean(self):
        if self.price is None or not(10_000 > self.price > 0):
            raise ValidationError("Please enter a valid price")
        if self.dish_type is None:
            raise ValidationError("Please enter a valid dish type")

    def __str__(self) -> str:
        return self.name

    def get_ingredients(self) -> QuerySet:
        return self.ingredients.all()

    def get_cooks(self) -> QuerySet:
        return self.cooks.all()

    def get_img(self) -> str:
        if Path(STATIC_URL + "img/" + self.name.lower() + ".jpg").exists():
            return "img/" + self.name.lower() + ".jpg"
        return "img/default.jpg"
