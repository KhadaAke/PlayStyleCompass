from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from .forms import CustomRegistrationForm, DeleteAccountForm, EmailChangeForm, CustomPasswordChangeForm, ProfilePictureForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages 


def register(request):
    """View function for user registration."""
    if request.method != 'POST':
        form = CustomRegistrationForm()
    else:
        form = CustomRegistrationForm(data=request.POST)
        
        if form.is_valid():
            # Check if a user with the provided email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'This email address is already in use.')
            else:
                new_user = form.save()
                # Log the user in and then redirect to the home page.
                login(request, new_user)
                return redirect('playstyle_compass:index')

    context = {
        'form': form,
        'page_title': 'Register :: PlayStyle Compass'
    }
    return render(request, 'registration/register.html', context)

@login_required
def delete_account(request):
    """View for deleting a user's account."""
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data['password']
            if request.user.check_password(password):
                request.user.delete()
                return redirect('users:login')
            else:
                form.add_error('password', 'Incorrect password. Please try again.')

    else:
        form = DeleteAccountForm()

    context = {
        'form': form,
        'page_title': 'Delete Account :: PlayStyle Compass'
    }

    return render(request, 'registration/delete_account.html', context)

@login_required
def change_email(request):
    """View for changing a user's email address."""
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, user=request.user)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            request.user.email = new_email
            request.user.save()
            
            messages.success(request, 'Your email has been updated successfully.')
            return redirect('playstyle_compass:index')
    else:
        form = EmailChangeForm(user=request.user, initial={'current_email': request.user.email})

    context = {
        'form': form,
        'page_title': 'Change Email :: PlayStyle Compass'
    }

    return render(request, 'registration/change_email.html', context)

@login_required
def change_password(request):
    """View for changing a user's password."""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['new_password1']
            password2 = form.cleaned_data['new_password2']

            if password1 == password2:
                if not request.user.check_password(password1):
                    request.user.set_password(password1)
                    request.user.save()

                    update_session_auth_hash(request, request.user)

                    return redirect('users:password_change_done')
                else:
                    messages.error(request, 'New password must be different from the old password.')
            else:
                form.add_error('new_password2', 'New passwords must match.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    context = {
        'form': form,
        'page_title': 'Change Password :: PlayStyle Compass'
    }

    return render(request, 'registration/password_change_form.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.userprofile)

        if form.is_valid():
            form.save()
            return redirect('users:profile')

    else:
        form = ProfilePictureForm(instance=request.user.userprofile)

    return render(request, 'registration/update_profile.html', {'form': form})
