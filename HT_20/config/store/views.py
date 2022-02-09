from datetime import datetime
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect

from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages
from django.urls import reverse
import requests

from store.forms import LoginForm, EditForm
from store.models import Category, Product, Cart


def index(request):
    context = {
        "date": datetime.now(),
        "categories": Category.objects.all(),
        "products": Product.objects.all(),
    }

    if request.user.is_authenticated:
        context["products_in_cart"] = [
            cart.product.pk for cart in Cart.objects.filter(user=request.user)]
        context["amount_products_in_cart"] = len(
            Cart.objects.filter(user=request.user))

    return render(request, "./store/index.html", context)


def category(request, pk):
    context = {
        "date": datetime.now(),
        "categories": Category.objects.all(),
        "products": Product.objects.filter(category=pk).all(),
    }

    if request.user.is_authenticated:
        context["products_in_cart"] = [
            cart.product.pk for cart in Cart.objects.filter(user=request.user)]
        context["amount_products_in_cart"] = len(
            Cart.objects.filter(user=request.user))

    return render(request, "./store/category.html", context)


def permission_denied(request):
    messages.warning(request, "У вас нет прав доступа")

    return HttpResponseRedirect(reverse('store:index'))


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

            return HttpResponseRedirect(reverse("store:category", kwargs={"pk": product.category.pk}))
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

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@ login_required
def cart(request):
    context = {
        "cart": Cart.objects.filter(user=request.user),
        "categories": Category.objects.all(),
        "date": datetime.now(),
        "amount_products_in_cart": len(Cart.objects.filter(user=request.user)),
    }

    return render(request, "./store/cart.html", context)


@ login_required
def add_product_from_cart(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
    except Http404:
        return HttpResponseNotFound()
    else:
        cart = Cart.objects.filter(user=request.user, product=product)
        if not cart:
            cart = Cart(user=request.user, product=product)
            cart.quantity = 1
            cart.save()

        messages.info(request, f"Товар \"{product.name}\" добавлен в корзину")

        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@ login_required
def remove_product_from_cart(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
    except Http404:
        return HttpResponseNotFound()
    else:
        cart = Cart.objects.filter(user=request.user, product=product)
        cart.delete()

        messages.info(request, f"Товар \"{product.name}\" удален с корзины")

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

                return HttpResponseRedirect(reverse('store:index'))
            else:
                messages.warning(request, 'Неверный логин или пароль')
        else:
            messages.warning(request, 'Форма заполнена некорректно')
    else:
        context["form"] = LoginForm()

    return render(request, "./store/login.html", context)


def logout_user(request):
    logout(request)

    return HttpResponseRedirect(reverse('store:index'))
