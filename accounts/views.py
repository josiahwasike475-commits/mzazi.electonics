from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def account(request):
    return render(request, "account.html", {"page_title": "Your account", "active_nav": "account"})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your Mzazi account is ready.")
            return redirect("accounts:account")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form, "page_title": "Create an account", "active_nav": "account"})
