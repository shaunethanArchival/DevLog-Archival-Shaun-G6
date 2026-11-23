from django.urls import path

from . import views

app_name = "tracker"

urlpatterns = [
    path("sessions/", views.session_list, name="session_list"),
    path("sessions/new/", views.session_create, name="session_create"),
    path("sessions/<int:pk>/edit/", views.session_update, name="session_update"),
    path("sessions/<int:pk>/delete/", views.session_delete, name="session_delete"),
    path("projects/", views.project_list, name="project_list"),
    path("projects/new/", views.project_create, name="project_create"),
    path("projects/<int:pk>/edit/", views.project_update, name="project_update"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project_delete"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
  
]
