from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from kitchen_app.forms import CookCreateForm, DishCreateForm, DishSearchForm
from kitchen_app.models import DishModel, CookModel, IngredientModel, DishTypeModel
from kitchen_service.settings import LOGIN_REDIRECT_URL


def index(request):
    context = {
        "dishes": DishModel.objects.all()[:3],
        "dish_count": DishModel.objects.count(),
        "cooks_count": CookModel.objects.count(),
        "ingredients_count": IngredientModel.objects.count(),
        "dish_types_count": DishTypeModel.objects.count()
    }

    return render(request, template_name="kitchen/index.html", context=context)


def login_view(request) -> HttpResponse:
    if request.method == "GET":
        context = {
            "username": request.session.get("username", ""),
            "password": request.session.get("password", "")
        }
        return render(request, template_name="registration/login.html", context=context)
    elif request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user =  authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                if request.POST.get("remember"):
                    request.session["username"] = username
                    request.session["password"] = password
                return redirect(LOGIN_REDIRECT_URL)
            else:
                return render(request, template_name="registration/login.html")
        return render(request, template_name="registration/login.html", context={"error": "Invalid username and/or password."})
    return render(request, template_name="registration/login.html")

class DishListView(ListView):
    model = DishModel
    template_name = "kitchen/dish/list.html"
    context_object_name = "dish_list"
    paginate_by = 5


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


class DishDetailView(DetailView, LoginRequiredMixin):
    model = DishModel
    template_name = "kitchen/dish/detail.html"
    fields = "__all__"
    context_object_name = "dish"


class DishCreateView(CreateView, LoginRequiredMixin):
    model = DishModel
    template_name = "kitchen/dish/create.html"
    success_url = reverse_lazy("kitchen_app:dishes")
    form_class = DishCreateForm


class DishUpdateView(UpdateView, LoginRequiredMixin):
    model = DishModel
    template_name = "kitchen/dish/create.html"
    success_url = reverse_lazy("kitchen_app:dishes")
    form_class = DishCreateForm


class DishDeleteView(DeleteView, LoginRequiredMixin):
    model = DishModel
    template_name = "kitchen/dish/delete.html"
    success_url = reverse_lazy("kitchen_app:dishes")


class IngredientListView(ListView):
    model = IngredientModel
    template_name = "kitchen/ingredient/list.html"


class IngredientCreateView(CreateView, LoginRequiredMixin):
    model = IngredientModel


class IngredientUpdateView(UpdateView, LoginRequiredMixin):
    model = IngredientModel
    fields = "__all__"
    template_name = "kitchen/ingredient/detail.html"


class IngredientDeleteView(DeleteView, LoginRequiredMixin):
    model = IngredientModel
    success_url = reverse_lazy("kitchen_app:ingredients")



class IngredientDetailView(DetailView, LoginRequiredMixin):
    model = IngredientModel
    template_name = "kitchen/ingredient/detail.html"


class CookCreateView(CreateView, LoginRequiredMixin):
    model = CookModel
    template_name = "registration/sign_up.html"
    success_url = reverse_lazy("index")
    form_class = CookCreateForm


class CookListView(ListView):
    model = CookModel
    template_name = "kitchen/cook/list.html"


class CookDetailView(DetailView, LoginRequiredMixin):
    model = CookModel


class UpdateCookView(UpdateView, LoginRequiredMixin):
    model = CookModel


class DeleteCookView(DeleteView, LoginRequiredMixin):
    model = CookModel



class DishTypeListView(ListView):
    model = DishTypeModel
    template_name = "kitchen/dish_type/list.html"


class DishTypeDetailView(DetailView, LoginRequiredMixin):
    model = DishTypeModel
    template_name = "kitchen/dish_type/detail.html"


class DishTypeCreateView(CreateView, LoginRequiredMixin):
    model = DishTypeModel
    fields = "__all__"
    template_name = "kitchen/dish_type/create.html"