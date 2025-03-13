from django.urls import path

from kitchen_app import views

urlpatterns = [
    path("", views.index, name="index"),
]

app_name = "kitchen_app"