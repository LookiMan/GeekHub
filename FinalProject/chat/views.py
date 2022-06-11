from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden, Http404, HttpResponseNotFound
from django.urls import reverse_lazy

from chat.forms import LoginStaffForm, RegisterStaffForm, ChangeStaffInfoForm
from chat.models import Staff, Chat


def superuser_required(view_func=None, login_url="chat:login"):
    actual_decorator = user_passes_test(
        lambda user: user.is_active and user.is_superuser,
        login_url=login_url,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


@login_required
def index(request):
    return render(request, "./chat/index.html", {})


@superuser_required
def archive(request, offset):
    return render(request, "./chat/archive.html", {})


def login_staff(request):
    context = {}

    if request.method == "POST":
        form = LoginStaffForm(request.POST)

        if form.is_valid():
            context["form"] = form
            login_data = form.cleaned_data

            user = authenticate(
                username=login_data["login"],
                password=login_data["password"],
            )
            if user:
                login(request, user)

                return redirect("chat:index")
            else:
                messages.warning(request, "Неверный логин или пароль")
        else:
            messages.warning(request, "Форма заполнена некорректно")
    else:
        context["form"] = LoginStaffForm()

    return render(request, "./chat/login.html", context)


def logout_staff(request):
    logout(request)

    return redirect("chat:index")


@superuser_required
def registration_staff(request):
    context = {}

    if request.method == "POST":
        form = RegisterStaffForm(request.POST)

        if form.is_valid():
            staff = form.save()

            Chat.objects.create(
                id=0,
                first_name="Мои заметки",
                last_name=None,
                username=None,
                is_note=True,
                staff=staff,
            )

            return redirect(reverse_lazy("chat:change_staff", kwargs={"pk": staff.pk}))

        else:
            context["form"] = RegisterStaffForm(request.POST or None)
            for error in form.errors.values():
                messages.warning(request, error)
    else:
        context["form"] = RegisterStaffForm()

    return render(request, "./chat/registration-staff.html", context)


@superuser_required
def change_staff(request, pk):
    context = {}

    try:
        staff = get_object_or_404(Staff, pk=pk)
    except Http404:
        return HttpResponseNotFound()
    else:
        if request.method == "POST":
            form = ChangeStaffInfoForm(
                request.POST or None, instance=staff)

            if form.is_valid():
                form.save()

                return redirect("chat:staff_list")

            else:
                context["form"] = ChangeStaffInfoForm(
                    request.POST or None, instance=staff)

                for error in form.errors.values():
                    messages.warning(request, error)
        else:
            context["form"] = ChangeStaffInfoForm(instance=staff)

        return render(request, "./chat/edit-staff.html", context)


@superuser_required
def staff_list(request):
    if request.method == "GET":
        context = {}
        try:
            formset = Staff.objects.all()
        except Exception as exc:
            messages.warning(request, f"Возникла непредвиденная ошибка: {exc}")
        else:
            context["formset"] = formset

        return render(request, "./chat/staff-list.html", context)
    else:
        return HttpResponseForbidden()
