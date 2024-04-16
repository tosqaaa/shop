from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'account/dashboard/dashboard.html', {'profile': profile})
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(data=request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return render(request, 'account/registration/register_done.html', context={'new_user': new_user})
        else:
            messages.error(request, 'Произошла ошибка регистрации')
            return redirect('account:register')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/registration/register.html', context={'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Изменения прошли успешно!')
        else:
            messages.error(request, 'Произошла ошибка редактирования!')
            return redirect('account:dashboard')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/edit.html', context=context)

@login_required
def delete(request):
    user = request.user
    user.delete()
    messages.success(request, 'Ваш аккаунт был удален!')
    return redirect('account:login')

