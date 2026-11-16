from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, ProfileUpdateForm, RegistrationForm


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    return redirect("accounts:login")


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in to continue.")
            return redirect("accounts:login")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect("accounts:dashboard")

            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("accounts:login")


@login_required
def dashboard_redirect(request):
    if request.user.role == "admin":
        return redirect("accounts:admin_dashboard")
    return redirect("accounts:member_dashboard")


@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        messages.error(request, "You do not have access to the admin dashboard.")
        return redirect("accounts:member_dashboard")

    return render(request, "accounts/dashboard_admin.html", {"user": request.user})


@login_required
def member_dashboard(request):
    if request.user.role != "member":
        messages.error(request, "You do not have access to the member dashboard.")
        return redirect("accounts:admin_dashboard")

    return render(request, "accounts/dashboard_member.html", {"user": request.user})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was updated successfully.")
            return redirect("accounts:profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form, "user": request.user})
