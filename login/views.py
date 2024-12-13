from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from dashboard.models import UserSchedule


# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin/')
        elif request.user.username.startswith("guest_"):
            return redirect('guest_page')
        elif not request.user.is_superuser:
            return redirect('normal_user_page')
        else:
            return redirect('admin_user_page')
    return render(request, "login/login.html")


def logout_view(request):
    logout(request)
    return redirect("/")


def guest_login(request):
    guest_username = "guest_" + get_random_string(8)
    guest_user = User.objects.create(username=guest_username)
    guest_user.set_unusable_password()
    guest_user.save()

    guest_user.backend = 'django.contrib.auth.backends.ModelBackend'

    login(request, guest_user)
    return redirect('guest_page')


def normal_user_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    if request.user.is_superuser:
        return render(request, "login/admin_user_page.html")
    else:
        user_schedule, created = UserSchedule.objects.get_or_create(user=request.user)
        assignments = user_schedule.assignments.all()

        sorting_token = request.session.get('sort_by', 'due_date')
        sorting_order = request.session.get('order', 'asc')

        if 'sort_by' in request.GET:
            sorting_token = request.GET['sort_by']
            request.session['sort_by'] = sorting_token
        if 'order' in request.GET:
            sorting_order = request.GET['order']
            request.session['order'] = sorting_order

        if sorting_order == 'asc':
            assignments = assignments.order_by(sorting_token)
        else:
            assignments = assignments.order_by(f'-{sorting_token}')

        return render(request, "login/normal_user_page.html", {'assignments': assignments})


def guest_page(request):
    if not request.user.is_authenticated or not request.user.username.startswith("guest_"):
        return redirect('login_page')
    return render(request, "login/guest_page.html")


def admin_user_page(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login_page')
    return render(request, 'login/admin_user_page.html')


@login_required
def profile(request):
    if request.user.username.startswith('guest'):
        return HttpResponseForbidden("Guest has no access to profile page")

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'login/profile.html', context)
