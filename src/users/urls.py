"""Defines URL patterns."""

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="account_actions/password_reset_form.html",
            subject_template_name="account_actions/password_reset_subject.txt",
            html_email_template_name="account_actions/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path("change_password/", views.change_password, name="change_password"),
    path("change_email/", views.change_email, name="change_email"),
    path("delete_account/", views.delete_account, name="delete_account"),
    path("profile/", views.update_profile, name="profile"),
    path(
        "change-profile-name/",
        views.ProfileUpdateView.as_view(),
        name="change_profile_name",
    ),
    path(
        "password_change-done/", views.change_password_done, name="change_password_done"
    ),
    path("change_email/done/", views.change_email_done, name="change_email_done"),
    path(
        "change_email/success", views.change_email_success, name="change_email_success"
    ),
    path("contact/", views.contact, name="contact"),
    path("contact_success/", views.contact_success, name="contact_success"),
    path(
        "resend-activation-link/",
        views.resend_activation_link,
        name="resend_activation_link",
    ),
    path(
        "confirm_email_change/<str:uidb64>/<str:token>/",
        views.confirm_email_change,
        name="confirm_email_change",
    ),
]
