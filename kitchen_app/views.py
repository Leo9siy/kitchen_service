from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from kitchen_app.forms import CookCreateForm
from kitchen_app.models import DishModel, CookModel, IngredientModel, DishTypeModel


def index(request):
    return render(request, template_name="kitchen/index.html")


class DishListView(ListView):
    model = DishModel
    template_name = "kitchen/dish/list.html"
    context_object_name = "dish_list"


    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            pk = request.POST.get("id")

            dish = DishModel.objects.get(
                pk=pk
            )
            if dish:
                new_name = request.POST.get("new_name")
                if new_name:
                    dish.name = request.POST.get("new_name")
                    dish.save()
                else:
                    dish.delete()

            return redirect("kitchen_app:dishes")


class DishDetailView(DetailView):
    model = DishModel
    template_name = "kitchen/dish/detail.html"
    fields = "__all__"
    context_object_name = "dish"


class DishCreateView(CreateView):
    model = DishModel
    fields = "__all__"
    template_name = "kitchen/dish/create.html"
    success_url = reverse_lazy("kitchen_app:dishes")


class DishUpdateView(UpdateView):
    model = DishModel


class DishDeleteView(DeleteView):
    model = DishModel


class IngredientListView(ListView):
    model = IngredientModel
    template_name = "kitchen/ingredient/list.html"


class IngredientCreateView(CreateView):
    model = IngredientModel


class IngredientUpdateView(UpdateView):
    model = IngredientModel
    fields = "__all__"
    template_name = "kitchen/ingredient/detail.html"


class IngredientDeleteView(DeleteView):
    model = IngredientModel
    success_url = reverse_lazy("kitchen_app:ingredients")



class IngredientDetailView(DetailView):
    model = IngredientModel
    template_name = "kitchen/ingredient/detail.html"


class CookCreateView(CreateView):
    model = CookModel
    template_name = "registration/sign_up.html"
    success_url = reverse_lazy("index")
    form_class = CookCreateForm


class CookListView(ListView):
    model = CookModel
    template_name = "kitchen/cook/list.html"


class CookDetailView(DetailView):
    model = CookModel


class UpdateCookView(UpdateView):
    model = CookModel


class DeleteCookView(DeleteView):
    model = CookModel



class DishTypeListView(ListView):
    model = DishTypeModel
    template_name = "kitchen/dish_type/list.html"


class DishTypeDetailView(DetailView):
    model = DishTypeModel
    template_name = "kitchen/dish_type/detail.html"