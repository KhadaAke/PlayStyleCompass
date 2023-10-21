"""Defines views."""


from django.shortcuts import render, redirect
from django.contrib.auth import (
    login,
    update_session_auth_hash,
)
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import LoginView

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)
from django.utils.encoding import (
    force_bytes,
    force_str,
)
from django.core.mail import EmailMessage
from django.utils.safestring import mark_safe
from django.http import JsonResponse, HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse

from .forms import (
    CustomRegistrationForm,
    DeleteAccountForm,
    EmailChangeForm,
    CustomPasswordChangeForm,
    ProfilePictureForm,
    ContactForm,
    CustomAuthenticationForm,
)

from .models import UserProfile
from .tokens import account_activation_token

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sessions.models import Session



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Custom user profile update view."""

    model = UserProfile
    template_name = "account_actions/profile_name_update.html"
    fields = ["profile_name"]

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_success_url(self):
        return reverse("playstyle_compass:index")


class CustomLoginView(LoginView):
    """Cusotm user login view."""

    authentication_form = CustomAuthenticationForm
    template_name = "registration/login.html"


def activate(request, uidb64, token):
    """Email activation view."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.userprofile.email_confirmed = True
        user.userprofile.save()
        user.save()

        messages.success(request, "Thank you for your email confirmation!")
        return redirect("playstyle_compass:index")
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect("playstyle_compass:index")


def activateEmail(request, user, to_email):
    """Send activation email to users."""
    mail_subject = "Activate your user account."
    message = render_to_string(
        "registration/activate_account.html",
        {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        message = (
            f"Hello <b>{user}</b>, please go to your email <b>{to_email}</b> inbox and click on "
            f"received activation link to confirm your registration. \
                  <b>Note:</b> If you cannot find the email in your inbox, we recommend checking your spam folder."
        )
        messages.success(request, mark_safe(message))
    else:
        messages.error(
            request,
            f"Problem sending email to {to_email}, check if you typed it correctly.",
        )


def resend_activation_link(request):
    """Resend email activation link to the user."""
    if request.method != "GET":
        return JsonResponse(
            {"success": False, "error_message": "Invalid request method"}
        )

    email = request.user.email
    user = User.objects.get(email=email)
    activateEmail(request, user, email)
    
    return JsonResponse({})


def register(request):
    """View function for user registration."""
    if request.method == "POST":
        form = CustomRegistrationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()

            user_profile = UserProfile(
                user=new_user,
                profile_name=form.cleaned_data["profile_name"],
            )

            user_profile.save()
            new_user.save()

            activateEmail(request, new_user, form.cleaned_data.get("email"))
            login(request, new_user)

            return redirect("playstyle_compass:index")

    else:
        form = CustomRegistrationForm()

    context = {"form": form, "page_title": "Register :: PlayStyle Compass"}

    return render(request, "registration/register.html", context)


@login_required
def delete_account(request):
    """View for deleting a user's account."""
    if request.method == "POST":
        form = DeleteAccountForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data["password"]
            if request.user.check_password(password):
                request.user.delete()
                messages.success(request, "Your account has been successfully deleted!")
                return redirect("playstyle_compass:index")
            else:
                form.add_error("password", "Incorrect password. Please try again.")

    else:
        form = DeleteAccountForm()

    context = {"form": form, "page_title": "Delete Account :: PlayStyle Compass"}

    return render(request, "account_actions/delete_account.html", context)


@login_required
def change_email(request):
    """View for email change with verification."""
    if request.method == "POST":
        form = EmailChangeForm(request.POST, user=request.user)
        if form.is_valid():
            new_email = form.cleaned_data["new_email"]
            token = default_token_generator.make_token(request.user)
            uid = urlsafe_base64_encode(force_bytes(request.user.pk))

            request.session['email_change_temp'] = new_email
            request.session['email_change_token'] = token

            confirm_url = request.build_absolute_uri(reverse("users:confirm_email_change", kwargs={"uidb64": uid, "token": token}))

            subject = "Confirm Email Change"
            from_email = settings.DEFAULT_FROM_EMAIL
            message = render_to_string("account_actions/confirm_email_change.txt", {"confirm_url": confirm_url, "new_email": new_email})
            send_mail(subject, message, from_email, [request.user.email])

            return redirect("users:change_email_done")
    else:
        form = EmailChangeForm(
            user=request.user, initial={"current_email": request.user.email}
        )

    context = {"form": form, "page_title": "Change Email :: PlayStyle Compass"}

    return render(request, "account_actions/change_email.html", context)

def confirm_email_change(request, uidb64, token):
    """View for email change confirmation."""
    if 'email_change_token' in request.session:
        user = request.user

        if request.session['email_change_token'] == token:
            user.email = request.session['email_change_temp']
            user.save()

            del request.session['email_change_temp']
            del request.session['email_change_token']

            return redirect("users:change_email_success")

    return HttpResponse("Invalid token for email change.")

@login_required
def change_email_success(request):
    """View for email change success."""
    new_email = request.user.email
    messages.success(request, "Email Address successfully changed!")
    context = {
        "page_title": "Email Change Success :: PlayStyle Compass",
        "response": "You have successfully changed your email address, go to the homepage by clicking the button below.",
        "additional_message": new_email,
    }
    return render(request, "account_actions/change_succeeded.html", context)


@login_required
def change_email_done(request):
    """View for email change confirmation."""
    messages.success(request, "Confirmation email successfully sent!")
    context = {
        "page_title": "Email Change Done :: PlayStyle Compass",
        "response": "An email confirmation has been sent to your current email address. Please check your inbox and click the link provided to confirm the email change.",
    }
    return render(request, "account_actions/change_succeeded.html", context)


@login_required
def change_password(request):
    """View for changing a user's password."""
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            password1 = form.cleaned_data["new_password1"]
            password2 = form.cleaned_data["new_password2"]

            if password1 == password2:
                if not request.user.check_password(password1):
                    request.user.set_password(password1)
                    request.user.save()

                    update_session_auth_hash(request, request.user)
                    return redirect("users:change_password_done")
                else:
                    messages.error(
                        request, "New password must be different from the old password!"
                    )
            else:
                form.add_error("new_password2", "New passwords must match.")
    else:
        form = CustomPasswordChangeForm(user=request.user)

    context = {
        "form": form,
        "page_title": "Change Password :: PlayStyle Compass",
    }

    return render(request, "account_actions/password_change_form.html", context)


@login_required
def change_password_done(request):
    """View for password change confirmation."""
    messages.success(request, "Password Changed Successfully!")
    context = {
        "page_title": "Password Change Done :: PlayStyle Compass",
        "response": "You have changed your password, go to the homepage by clicking the button below.",
    }
    return render(request, "account_actions/change_succeeded.html", context)


@login_required
def update_profile(request):
    """View for profile image update."""
    if request.method == "POST":
        form = ProfilePictureForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )

        if form.is_valid():
            form.save()
            return redirect("users:profile")

    else:
        form = ProfilePictureForm(instance=request.user.userprofile)

    context = {
        "form": form,
        "page_title": "Change Profile Picture :: PlayStyle Compass",
    }

    return render(request, "account_actions/update_profile.html", context)


def contact(request):
    """Contact view."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            subject = "New Conctat Us Submission"
            message = f"""
                Name: {contact_message.name}
                Email: {contact_message.email}
                Subject: {contact_message.subject}
                Message: {contact_message.message}
                Time: {contact_message.formatted_timestamp()}
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.EMAIL_USER_CONTACT]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return redirect("users:contact_success")
    else:
        form = ContactForm()

    context = {"form": form, "page_title": "Contact Us :: PlayStyle Compass"}

    return render(request, "account_actions/contact.html", context)


def contact_success(request):
    """Contact confirmation view."""
    messages.success(request, "Your message has been successfully submitted!")
    context = {
        "page_title": "Contact Us Done :: PlayStyle Compass",
        "response": "Thank you for contacting us! Our team will review it within 48 hours and get back to you as soon as possible. \
    Go to the homepage by clicking the button below.",
    }
    return render(request, "account_actions/change_succeeded.html", context)
