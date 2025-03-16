from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from kitchen_app.forms import CookCreateForm, DishCreateForm, DishSearchForm
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

            if pk:
                dish = DishModel.objects.get(
                    pk=pk
                )
                new_name = request.POST.get("new_name")
                if new_name:
                    dish.name = request.POST.get("new_name")
                    dish.save()
                else:
                    dish.delete()

            return redirect("kitchen_app:dishes")

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super(DishListView, self).get_context_data(**kwargs)

        if self.request.method == "GET":
            dish_name = self.request.GET.get("dish_name", "")
            context["dish_name"] = dish_name

            context["search"] = DishSearchForm(
                initial={"dish_name": dish_name}
            )
        return context

    def get_queryset(self):
        query_set = DishModel.objects.all().select_related("dish_type").prefetch_related("ingredients")
        if self.request.method == "GET":
            form = DishSearchForm(self.request.GET)
            if form.is_valid():
                return query_set.filter(name__icontains=form.cleaned_data["dish_name"])

        return query_set


class DishDetailView(DetailView):
    model = DishModel
    template_name = "kitchen/dish/detail.html"
    fields = "__all__"
    context_object_name = "dish"


class DishCreateView(CreateView):
    model = DishModel
    template_name = "kitchen/dish/create.html"
    success_url = reverse_lazy("kitchen_app:dishes")
    form_class = DishCreateForm


class DishUpdateView(UpdateView):
    model = DishModel
    template_name = "kitchen/dish/create.html"
    success_url = reverse_lazy("kitchen_app:dishes")
    form_class = DishCreateForm


class DishDeleteView(DeleteView):
    model = DishModel
    template_name = "kitchen/dish/delete.html"
    success_url = reverse_lazy("kitchen_app:dishes")



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