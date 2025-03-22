from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class DishTypeModel(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class CookModel(AbstractUser):
    year_of_experience = models.IntegerField(default=0)
    username = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


class IngredientModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DishModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)

    dish_type = models.ForeignKey(DishTypeModel, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(IngredientModel, related_name='dish_ingredients')
    cooks = models.ManyToManyField(CookModel, related_name='dishes')

    class Meta:
        ordering = ['price']


    def __str__(self):
        return self.name

    def clean(self):
        if self.ingredients.count() == 0:
            raise ValidationError('ingredients must have at least one ingredient')
        if self.cooks.count() == 0:
            raise ValidationError('cooks must have at least one cook')
        if self.price <= 0:
            raise ValidationError('price must be greater than zero')

    def get_ingredients(self):
        return self.ingredients.all()

    def get_cooks(self):
        return self.cooks.all()

    def get_img(self):
        return "img/" + self.name.lower() + ".jpg"


