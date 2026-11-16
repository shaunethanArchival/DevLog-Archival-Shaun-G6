from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.home_redirect, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_redirect, name="dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/member/", views.member_dashboard, name="member_dashboard"),
    path("profile/", views.profile_view, name="profile"),
]
