from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page, name="login_page"),
    path("logout", views.logout_view, name="logout"),
    path("guest_login", views.guest_login, name="guest_login"),
    path("admin_user_page", views.admin_user_page, name="admin_user_page"),
    path("normal_user_page", views.normal_user_page, name="normal_user_page"),
    path("guest_page", views.guest_page, name="guest_page"),
    path("profile", views.profile, name="profile"),
]