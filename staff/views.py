from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone

from .forms import StaffLoginForm, StaffForm
from .models import Staff

from vehicle.forms import CategoryForm, RegistrationForm, CheckOutForm
from vehicle.models import Category, Registration


def loginPage(request):

    form = StaffLoginForm(request, data=request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.role == "ADMIN":
                return redirect("report_dashboard")

            elif user.role == "ATTENDANT":
                return redirect("dashboard")

            elif user.role == "MANAGER":
                return redirect("tyre_list")

            return redirect("dashboard")

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'loginpage.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('loginPage')


def register_user(request):

    if request.user.role != "ADMIN":
        return render(request, "403.html", {"message": "Access denied"})

    form = StaffForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('user_list')

    return render(request, 'user_registration.html', {'form': form})


def user_list(request):

    if request.user.role != "ADMIN":
        return render(request, "403.html", {"message": "Access denied"})

    users = Staff.objects.all().order_by("-date_joined")
    return render(request, "user_list.html", {"users": users})


def edit_user(request, pk):

    if request.user.role != "ADMIN":
        return render(request, "403.html", {"message": "Access denied"})

    user = get_object_or_404(Staff, id=pk)
    form = StaffForm(request.POST or None, instance=user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('user_list')

    return render(request, 'edit_user.html', {'form': form})


def delete_user(request, id):

    if request.user.role != "ADMIN":
        return render(request, "403.html", {"message": "Access denied"})

    user = get_object_or_404(Staff, id=id)

    if request.method == "POST":
        user.delete()
        return redirect('user_list')

    return render(request, 'delete_user.html', {'user': user})


