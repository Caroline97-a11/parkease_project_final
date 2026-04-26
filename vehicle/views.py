from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from vehicle.forms import CategoryForm, RegistrationForm, CheckOutForm
from .models import Category, Registration

# Create your views here.
def no_access():
    return HttpResponseForbidden(" You do not have permission to access this page.")


def vehicle_category(request):
    if request.user.role != "ADMIN":
        return no_access()

    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicle_category_list')

    return render(request, 'category/eadd_category.html', {'form': form})


def vehicle_category_list(request):
    if request.user.role != "ADMIN" and request.user.role != "ATTENDANT":
        return no_access()
    else:

        categories = Category.objects.all()
        return render(request, "vehicle_category.html", {"categories": categories})


def register_vehicle(request):
    if request.user.role != "ATTENDANT":
        return no_access()

    form =RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.arrival_time = timezone.now()
            vehicle.status = "parked"
            vehicle.save()
            return redirect('dashboard')

    return render(request, 'vehicle/register.html', {'form': form})


def dashboard(request):
    if request.user.role not in ["ADMIN", "ATTENDANT"]:
        return no_access()

    all_vehicles = Registration.objects.all().order_by("-arrival_time")

    if request.user.role == "ATTENDANT":
        parked_vehicles = all_vehicles.filter(status="parked")
        signed_out_vehicles = all_vehicles.filter(status="signed_out")

    elif request.user.role == "ADMIN":
        parked_vehicles = all_vehicles.filter(status="parked")
        signed_out_vehicles = all_vehicles.filter(status="signed_out")

  #count for cards
    total_vehicles = all_vehicles.count()
    parked = parked_vehicles.count()
    checked_out = signed_out_vehicles.count()

# card logic for  the dashboard
    cards = [
        {
            "title": "Total Vehicles",
            "value": total_vehicles,
            "icon": "bi-car-front",
            "text_color": "text-primary",
        },
        {
            "title": "Currently Parked",
            "value": parked,
            "icon": "bi-check-circle",
            "text_color": "text-success",
        },
        {
            "title": "Checked Out",
            "value": checked_out,
            "icon": "bi-box-arrow-right",
            "text_color": "text-dark",
        },
    ]

    context = {
        "cards": cards,
        "parked_vehicles": parked_vehicles,
        "signed_out_vehicles": signed_out_vehicles,
    }

    return render(request, "vehicle/dashboard.html", context)

def checkout_vehicle(request, pk):
    if request.user.role != "ATTENDANT":
        return no_access()

    vehicle = get_object_or_404(Registration, id=pk)

    now = timezone.now()
    duration = (now - vehicle.arrival_time).total_seconds() / 3600

    category = vehicle.vehicle_type

    if duration < 3:
        fee = category.short
        rate_type = "short"
    else:
        hour = timezone.localtime(now).hour
        if 6 <= hour < 19:
            fee = category.day
            rate_type = "day"
        else:
            fee = category.night
            rate_type = "night"

    if request.method == "POST":
        form = CheckOutForm(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle.departure_time = now
            vehicle.fee = fee
            vehicle.rate_type = rate_type
            vehicle.status = "signed_out"
            vehicle.save()
            return redirect("dashboard")
    else:
        form = CheckOutForm(instance=vehicle)

    return render(request, "vehicle/exit.html", {
        "vehicle": vehicle,
        "form": form,
        "duration": round(duration, 2),
        "fee": fee,
        "rate_type": rate_type
    })


def vehicle_receipt(request, pk):
    if request.user.role not in ["ADMIN", "ATTENDANT"]:
        return no_access()

    vehicle = get_object_or_404(Registration, id=pk)

    # Calculating duration
    if vehicle.departure_time and vehicle.arrival_time:
        duration = (vehicle.departure_time - vehicle.arrival_time).total_seconds() / 3600
    else:
        duration = 0

    context = {
        "vehicle": vehicle,
        "hours": round(duration, 2),
        "fee": vehicle.fee,
        "rate_type": vehicle.rate_type or "pending"
    }

    return render(request, "receipt.html", context)


@login_required
def edit_vehicle(request, id):
    vehicle = get_object_or_404(Registration, id=id)

    if vehicle.status != "parked":
        messages.error(request, "You cannot edit a signed-out vehicle.")
        return redirect('dashboard')

    if request.method == "POST":
        form = RegistrationForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle updated successfully.")
            return redirect('vehicle/dashboard')
    else:
        form = RegistrationForm(instance=vehicle)

    return render(request, 'vehicle/edit_vehicle.html', {'form': form})

def edit_category(request, id):
    category = get_object_or_404(Category, id=id)

    form = CategoryForm(request.POST or None, instance=category)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('category_list')

    context = {
        "form": form
    }

    return render(request, "category/edit_category.html", context)


def delete_category(request, id):
    category = get_object_or_404(Category, id=id)

    if request.method == "POST":
        category.delete()
        return redirect('category_list')

    return render(request, "category/delete_category.html", {"category": category})

