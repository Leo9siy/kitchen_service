from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)

from kitchen_app.forms import (
    CookCreateForm,
    DishCreateForm,
    DishSearchForm,
    CookSearchForm,
    IngredientSearchForm,
    DishTypeSearchForm,
)
from kitchen_app.models import (DishModel, CookModel,
                                IngredientModel, DishTypeModel)
from kitchen_service.settings.base import LOGIN_REDIRECT_URL


def index(request: HttpRequest):
    context = {
        "dishes": DishModel.objects.all()[:3],
        "dish_count": DishModel.objects.count(),
        "cooks_count": CookModel.objects.count(),
        "ingredients_count": IngredientModel.objects.count(),
        "dish_types_count": DishTypeModel.objects.count(),
    }

    return render(request, template_name="kitchen/index.html", context=context)


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        context = {
            "username": request.session.get("username", ""),
            "password": request.session.get("password", ""),
        }
        return render(
            request,
            template_name="registration/login.html",
            context=context
        )
    elif request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                if request.POST.get("remember"):
                    request.session["username"] = username
                    request.session["password"] = password
                return redirect(LOGIN_REDIRECT_URL)
            else:
                return render(request, template_name="registration/login.html")
        return render(
            request,
            template_name="registration/login.html",
            context={"error": "Invalid username and/or password."},
        )
    return render(request, template_name="registration/login.html")


class DishListView(ListView):
    model = DishModel
    template_name = "kitchen/dish/list.html"
    context_object_name = "dish_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=..., **kwargs) -> dict:
        context = super(DishListView, self).get_context_data(**kwargs)

        if self.request.method == "GET":
            dish_name = self.request.GET.get("dish_name", "")
            context["dish_name"] = dish_name

            context["search"] = DishSearchForm(
                initial={"dish_name": dish_name}
            )
        return context

    def get_queryset(self) -> QuerySet:
        query_set = (
            DishModel.objects.all()
            .select_related("dish_type")
            .prefetch_related("ingredients")
        )
        if self.request.method == "GET":
            form = DishSearchForm(self.request.GET)
            if form.is_valid():
                return query_set.filter(
                    name__icontains=form.cleaned_data["dish_name"]
                )

        return query_set


class DishDetailView(DetailView):
    model = DishModel
    template_name = "kitchen/dish/detail.html"
    fields = "__all__"
    context_object_name = "dish"


class DishCreateView(LoginRequiredMixin, CreateView):
    model = DishModel
    template_name = "kitchen/dish/create.html"
    success_url = reverse_lazy("kitchen_app:dishes")
    form_class = DishCreateForm


class DishUpdateView(LoginRequiredMixin, UpdateView):
    model = DishModel
    template_name = "kitchen/dish/create.html"
    success_url = reverse_lazy("kitchen_app:dishes")
    form_class = DishCreateForm


class DishDeleteView(LoginRequiredMixin, DeleteView):
    model = DishModel
    template_name = "kitchen/dish/delete.html"
    success_url = reverse_lazy("kitchen_app:dishes")
    context_object_name = "dish"


class IngredientListView(ListView):
    model = IngredientModel
    template_name = "kitchen/ingredient/list.html"
    context_object_name = "ingredient_list"
    paginate_by = 5

    def post(self, request, *args, **kwargs) -> HttpResponseRedirect | None:
        context = request.POST.copy()
        if "pk" in context:
            ingredient = IngredientModel.objects.get(pk=context["pk"])

            if "new_name" in context:
                new_name = context["new_name"]
                if len(new_name) > 0:
                    ingredient.name = new_name
                    ingredient.save()
            else:
                ingredient.delete()

            return redirect("kitchen_app:ingredients")

    def get_queryset(self) -> QuerySet:
        query_set = IngredientModel.objects.all()
        if self.request.method == "GET":
            form = IngredientSearchForm(self.request.GET)
            if form.is_valid():
                name = form.cleaned_data["ingredient_name"]
                return query_set.filter(name__icontains=name)
        return query_set

    def get_context_data(self, *, object_list=..., **kwargs) -> dict:
        context = super(IngredientListView, self).get_context_data(**kwargs)
        if self.request.method == "GET":
            ingredient_name = self.request.GET.get("ingredient_name", "")
            context["ingredient_name"] = ingredient_name
            context["search"] = IngredientSearchForm(
                initial={"ingredient_name": ingredient_name}
            )
        return context


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = IngredientModel
    fields = "__all__"
    template_name = "kitchen/ingredient/create.html"
    success_url = reverse_lazy("kitchen_app:ingredients")


class CookCreateView(CreateView):
    model = CookModel
    template_name = "registration/sign_up.html"
    success_url = reverse_lazy("index")
    form_class = CookCreateForm


class CookListView(ListView):
    model = CookModel
    template_name = "kitchen/cook/list.html"
    context_object_name = "cook_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=..., **kwargs) -> dict:
        context = super(CookListView, self).get_context_data(**kwargs)
        if self.request.method == "GET":
            cook_name = self.request.GET.get("cook_name", "")
            context["cook_name"] = cook_name
            context["search"] = CookSearchForm(
                initial={"cook_name": cook_name}
            )
        return context

    def get_queryset(self) -> QuerySet:
        query_set = CookModel.objects.all()
        if self.request.method == "GET":
            form = CookSearchForm(self.request.GET)
            if form.is_valid():
                return query_set.filter(
                    username__icontains=form.cleaned_data["cook_name"]
                )
        return query_set


class CookDetailView(LoginRequiredMixin, DetailView):
    model = CookModel
    template_name = "kitchen/cook/detail.html"
    context_object_name = "cook"


class CookUpdateView(LoginRequiredMixin, UpdateView):
    model = CookModel
    template_name = "kitchen/cook/update.html"
    context_object_name = "cook"
    fields = ("username", "year_of_experience")
    success_url = reverse_lazy("kitchen_app:cookers")


class CookDeleteView(LoginRequiredMixin, DeleteView):
    model = CookModel
    template_name = "kitchen/cook/delete.html"
    success_url = reverse_lazy("kitchen_app:cooks")
    context_object_name = "cook"


class DishTypeListView(ListView):
    model = DishTypeModel
    template_name = "kitchen/dish_type/list.html"
    context_object_name = "dish_type_list"
    paginate_by = 5

    def post(
            self, request: HttpRequest,
            *args, **kwargs
    ) -> HttpResponseRedirect | None:
        context = request.POST.copy()
        if "pk" in context:
            dish_type = DishTypeModel.objects.get(pk=context["pk"])

            if "new_name" in context:
                new_name = context["new_name"]
                if len(new_name) > 0:
                    dish_type.name = new_name
                    dish_type.save()
            else:
                dish_type.delete()

            return redirect("kitchen_app:dish_types")

    def get_queryset(self) -> QuerySet:
        query_set = DishTypeModel.objects.all()
        if self.request.method == "GET":
            form = DishTypeSearchForm(self.request.GET)
            if form.is_valid():
                return query_set.filter(
                    name__icontains=form.cleaned_data["type_name"]
                )
        return query_set

    def get_context_data(self, *, object_list=..., **kwargs) -> dict:
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        if self.request.method == "GET":
            dish_type_name = self.request.GET.get("type_name", "")
            context["type_name"] = dish_type_name
            context["search"] = DishTypeSearchForm(
                initial={"type_name": dish_type_name}
            )
        return context


class DishTypeCreateView(LoginRequiredMixin, CreateView):
    model = DishTypeModel
    fields = "__all__"
    template_name = "kitchen/dish_type/create.html"
    success_url = reverse_lazy("kitchen_app:dish_types")
