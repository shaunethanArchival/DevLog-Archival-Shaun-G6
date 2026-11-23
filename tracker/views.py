from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, ProjectForm, WorkSessionForm
from .models import Category, Project, WorkSession


def _is_admin(user):
    """Admin role: checks a custom `role` field (on user or profile) first, then Django staff flags.
    Adjust to match your accounts app."""
    role = getattr(user, "role", None) or getattr(getattr(user, "profile", None), "role", None)
    if role:
        return str(role).lower() == "admin"
    return user.is_staff or user.is_superuser


def _get_session(request, pk):
    """Owner can edit/delete; admin role may manage any session; everyone else gets 404."""
    if _is_admin(request.user):
        return get_object_or_404(WorkSession, pk=pk)
    return get_object_or_404(WorkSession, pk=pk, user=request.user)


# ---------- Work sessions (core feature) ----------
@login_required
def session_list(request):
    sessions = WorkSession.objects.select_related("project")
    if not _is_admin(request.user):          # members only see their own records
        sessions = sessions.filter(user=request.user)
    project_id = request.GET.get("project")
    if project_id and project_id.isdigit():
        sessions = sessions.filter(project_id=project_id)
    total = sessions.aggregate(t=Sum("duration_minutes"))["t"] or 0
    projects = Project.objects.filter(user=request.user)
    return render(request, "tracker/session_list.html", {
        "sessions": sessions, "projects": projects, "total_minutes": total,
        "total_hours": round(total / 60, 1), "selected": project_id, "is_admin": _is_admin(request.user),
    })


@login_required
def session_create(request):
    form = WorkSessionForm(request.POST or None, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user          # linked to the creator
            session.save()
            messages.success(request, "Work session logged.")
            return redirect("tracker:session_list")
        messages.error(request, "Please fix the errors below.")
    return render(request, "tracker/session_form.html", {"form": form, "title": "Log a work session"})


@login_required
def session_update(request, pk):
    session = _get_session(request, pk)
    form = WorkSessionForm(request.POST or None, instance=session, user=session.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Work session updated.")
            return redirect("tracker:session_list")
        messages.error(request, "Please fix the errors below.")
    return render(request, "tracker/session_form.html", {"form": form, "title": "Edit work session"})


@login_required
def session_delete(request, pk):
    session = _get_session(request, pk)
    if request.method == "POST":
        session.delete()
        messages.success(request, "Work session deleted.")
        return redirect("tracker:session_list")
    return render(request, "tracker/confirm_delete.html", {"object": session, "back": "tracker:session_list"})


# ---------- Projects ----------
@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user).annotate(
        session_count=Count("sessions"), minutes=Sum("sessions__duration_minutes"))
    return render(request, "tracker/project_list.html", {"projects": projects})


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            form.save_m2m()
            messages.success(request, "Project created.")
            return redirect("tracker:project_list")
        messages.error(request, "Please fix the errors below.")
    return render(request, "tracker/session_form.html", {"form": form, "title": "New project"})


@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    form = ProjectForm(request.POST or None, instance=project, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated.")
            return redirect("tracker:project_list")
        messages.error(request, "Please fix the errors below.")
    return render(request, "tracker/session_form.html", {"form": form, "title": "Edit project"})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project and its sessions deleted.")
        return redirect("tracker:project_list")
    return render(request, "tracker/confirm_delete.html", {"object": project, "back": "tracker:project_list"})


# ---------- Categories ----------
@login_required
def category_list(request):
    form = CategoryForm(request.POST or None, user=request.user)
    if request.method == "POST":
        if form.is_valid():
            c = form.save(commit=False)
            c.user = request.user
            c.save()
            messages.success(request, "Category added.")
            return redirect("tracker:category_list")
        messages.error(request, "Please fix the errors below.")
    categories = Category.objects.filter(user=request.user)
    return render(request, "tracker/category_list.html", {"form": form, "categories": categories})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted.")
        return redirect("tracker:category_list")
    return render(request, "tracker/confirm_delete.html", {"object": category, "back": "tracker:category_list"})
