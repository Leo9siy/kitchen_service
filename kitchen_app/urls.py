from django.urls import path

from kitchen_app import views
from kitchen_app.views import (
    CookCreateView,
    CookListView,
    CookDetailView,
    DishListView,
    DishCreateView,
    DishDetailView,
    DishTypeListView,
    IngredientListView,
    IngredientCreateView,
    DishUpdateView,
    DishDeleteView,
    DishTypeCreateView,
    CookDeleteView,
    CookUpdateView,
)

urlpatterns = [
    path("", views.index, name="index"),
    path("cooks/", CookListView.as_view(), name="cookers"),
    path("cooks/create/", CookCreateView.as_view(), name="cooker_create"),
    path(
        "cooks/<int:pk>/delete/",
        CookDeleteView.as_view(),
        name="cook_delete"
    ),
    path(
        "cooks/<int:pk>/update/",
        CookUpdateView.as_view(),
        name="cook_update"
    ),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cooker_detail"),
    path("dishes/", DishListView.as_view(), name="dishes"),
    path("dish/create/", DishCreateView.as_view(), name="dish_create"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish_detail"),
    path("dish/<int:pk>/update", DishUpdateView.as_view(), name="dish_update"),
    path("dish/<int:pk>/delete", DishDeleteView.as_view(), name="dish_delete"),
    path("dish-types/", DishTypeListView.as_view(), name="dish_types"),
    path(
        "dish-type/create/",
        DishTypeCreateView.as_view(),
        name="dish_type_create"
    ),
    path(
        "ingredients/",
        IngredientListView.as_view(),
        name="ingredients"
    ),
    path(
        "ingredient/create/",
        IngredientCreateView.as_view(),
        name="ingredient_create"
    ),
]

app_name = "kitchen_app"
