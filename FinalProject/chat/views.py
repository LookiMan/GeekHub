from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import Http404, HttpResponseNotFound
from django.urls import reverse_lazy

from chat.forms import LoginStaffForm, RegisterStaffForm, ChangeStaffInfoForm
from chat.models import Staff
from telegram_bot.models import Chat


@login_required
def index(request):
    context = {}
    return render(request, "./chat/index.html", context)


def login_staff(request):
    context = {}

    if request.method == "POST":
        form = LoginStaffForm(request.POST)

        if form.is_valid():
            context["form"] = form
            login_data = form.cleaned_data

            user = authenticate(
                username=login_data['login'],
                password=login_data['password'],
            )
            if user:
                login(request, user)

                return redirect('chat:index')
            else:
                messages.warning(request, 'Неверный логин или пароль')
        else:
            messages.warning(request, 'Форма заполнена некорректно')
    else:
        context["form"] = LoginStaffForm()

    return render(request, "./chat/login.html", context)


def logout_staff(request):
    logout(request)

    return redirect('chat:index')


@ user_passes_test(lambda staff: staff.is_superuser, login_url='chat:login')
def registration_staff(request):
    context = {}

    if request.method == "POST":
        form = RegisterStaffForm(request.POST)

        if form.is_valid():
            staff = form.save()

            Chat.objects.get_or_create(
                id=0,
                first_name="Мои заметки",
                last_name=None,
                username=None,
                staff=staff,
            )

            return redirect(reverse_lazy('chat:edit', kwargs={"pk": staff.pk}))

        else:
            context["form"] = RegisterStaffForm()
            for error in form.errors.values():
                messages.warning(request, error)
    else:
        context["form"] = RegisterStaffForm()

    return render(request, "./chat/registration_staff.html", context)


@ user_passes_test(lambda staff: staff.is_superuser, login_url='chat:login')
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

                return redirect('chat:index')

            else:
                context["form"] = ChangeStaffInfoForm(
                    request.POST or None, instance=staff)

                for error in form.errors.values():
                    messages.warning(request, error)
        else:
            context["form"] = ChangeStaffInfoForm(instance=staff)

        return render(request, "./chat/edit_staff.html", context)
