from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from kitchen_app import models

# Register your models here.

admin.site.unregister(Group)


@admin.register(models.CookModel)
class CookModelAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("year_of_experience",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {"fields": ("year_of_experience", "first_name", "last_name")},
        ),
    )


@admin.register(models.DishModel)
class DishModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "dish_type",
    )
    list_filter = ["dish_type__name", "name"]
    search_fields = ["name"]


admin.site.register(models.DishTypeModel)
admin.site.register(models.IngredientModel)
