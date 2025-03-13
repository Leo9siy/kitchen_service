from django.contrib.auth.models import AbstractUser
from django.db import models


class DishType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class CookModel(AbstractUser):
    year_of_experience = models.IntegerField(default=0)
    username = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.username


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class DishModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)

    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, related_name='dish_ingredients')
    cooks = models.ManyToManyField(CookModel, related_name='dishes')

    def __str__(self):
        return self.name
