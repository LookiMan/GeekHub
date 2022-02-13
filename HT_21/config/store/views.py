from datetime import datetime

from django.http import Http404, HttpResponseRedirect, HttpResponseNotFound, JsonResponse

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from store.forms import LoginForm, EditForm
from store.models import Category, Product
from store.utils import Cart
from store.serializers import ProductSerializer


def index(request):
    context = {
        "date": datetime.now(),
        "categories": Category.objects.all(),
        "products": Product.objects.all(),
    }

    if request.user.is_authenticated:
        cart = Cart(request)
        context["cart"] = cart

    return render(request, "./store/index.html", context)


def category(request, pk):
    context = {
        "date": datetime.now(),
        "categories": Category.objects.all(),
        "products": Product.objects.filter(category=pk).all(),
    }

    if request.user.is_authenticated:
        cart = Cart(request)
        context["cart"] = cart

    return render(request, "./store/category.html", context)


def permission_denied(request):
    messages.warning(request, "У вас нет прав доступа")

    return redirect('store:index')


@ user_passes_test(lambda u: u.is_superuser, login_url='store:permission_denied')
def edit_product(request, pk):
    context = {
        "date": datetime.now()
    }

    try:
        product = get_object_or_404(Product, pk=pk)
    except Http404:
        return HttpResponseNotFound()
    else:
        if request.method == "POST":
            form = EditForm(request.POST or None, instance=product)

            if form.is_valid():
                form.save()

            return redirect("store:category", kwargs={"pk": product.category.pk})
        else:
            context["form"] = EditForm(request.POST or None, instance=product)

            return render(request, "./store/edit.html", context)


@ user_passes_test(lambda u: u.is_superuser, login_url='store:permission_denied')
def delete_product(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
    except Http404:
        return HttpResponseNotFound()
    else:
        product.delete()

        messages.info(request, f"Товар \"{product.name}\" удален")

        return redirect(request.META.get("HTTP_REFERER"))


@ login_required
def cart(request):
    cart = Cart(request)
    context = {
        "cart": cart,
        "categories": Category.objects.all(),
        "date": datetime.now(),
    }

    return render(request, "./store/cart.html", context)


@ login_required
def add_product_to_cart(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
    except Http404:
        return JsonResponse({"message": f"Не удалось добавить даный товар в корзину"}, status=404)
    else:
        cart = Cart(request)
        cart.add(product=product)

        if request.method == "POST":
            response = {
                "message": f"Товар \"{product.name}\" добавлен в корзину",
                "amount_products": cart.amount_products,
            }

            return JsonResponse(response, status=200)

        else:
            messages.info(
                request, f"Товар \"{product.name}\" добавлен в корзину")

            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@ login_required
def remove_product_from_cart(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
    except Http404:
        return JsonResponse({"message": f"Не удалось удалить даный товар с корзины"}, status=404)
    else:
        cart = Cart(request)
        cart.remove(product)

        if request.method == "POST":
            response = {
                "message": f"Товар \"{product.name}\" удален с корзины",
                "amount_products": cart.amount_products,
            }

            return JsonResponse(response, status=200)

        else:
            messages.info(request, f"Товар \"{product.name}\" удален")

            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def login_user(request):
    context = {
        "date": datetime.now(),
    }

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            context["form"] = form
            login_data = form.cleaned_data

            user = authenticate(
                username=login_data['username'],
                password=login_data['password']
            )
            if user:
                login(request, user)

                return redirect('store:index')
            else:
                messages.warning(request, 'Неверный логин или пароль')
        else:
            messages.warning(request, 'Форма заполнена некорректно')
    else:
        context["form"] = LoginForm()

    return render(request, "./store/login.html", context)


def logout_user(request):
    logout(request)

    return redirect('store:index')


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
