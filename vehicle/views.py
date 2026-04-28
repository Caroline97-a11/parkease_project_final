from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseForbidden
from vehicle.forms import CategoryForm, RegistrationForm, CheckOutForm
from .models import Category, Registration


def no_access():
    # Returns a forbidden response when user has no permission
    return HttpResponseForbidden("You do not have permission to access this page.")


def vehicle_category(request):
    if not request.user.is_authenticated or request.user.role != "ADMIN":
        return no_access()

    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect("vehicle_category_list")

    return render(request, "category/add_category.html", {"form": form})


def vehicle_category_list(request):
    if not request.user.is_authenticated or request.user.role not in ["ADMIN", "ATTENDANT"]:
        return no_access()

    categories = Category.objects.all()
    return render(request, "category/category_list.html", {"categories": categories})


def edit_category(request, id):
    if not request.user.is_authenticated or request.user.role != "ADMIN":
        return no_access()

    category = get_object_or_404(Category, id=id)
    form = CategoryForm(request.POST or None, instance=category)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect("vehicle_category_list")

    return render(request, "category/edit_category.html", {"form": form})


def delete_category(request, id):
    if not request.user.is_authenticated or request.user.role != "ADMIN":
        return no_access()

    category = get_object_or_404(Category, id=id)

    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect("vehicle_category_list")

    return render(request, "category/delete_category.html", {"category": category})


# VEHICLE REGISTRATION

def register_vehicle(request):
    if not request.user.is_authenticated or request.user.role != "ATTENDANT":
        return no_access()

    form = RegistrationForm()

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)

            vehicle.arrival_time = timezone.now()
            vehicle.status = "parked"
            vehicle.registered_by = request.user
            vehicle.save()

            messages.success(request, "Vehicle registered successfully.")
            return redirect("dashboard")

    return render(request, "vehicle/register_vehicle.html", {"form": form})



# DASHBOARD

def dashboard(request):
    if not request.user.is_authenticated or request.user.role not in ["ADMIN", "ATTENDANT"]:
        return no_access()

    all_vehicles = Registration.objects.all().order_by("-arrival_time")

    parked_vehicles = all_vehicles.filter(status="parked")
    signed_out_vehicles = all_vehicles.filter(status="signed_out")

    cards = [
        {"title": "Total Vehicles", "value": all_vehicles.count(),
         "icon": "bi-car-front", "text_color": "text-primary"},
        {"title": "Currently Parked", "value": parked_vehicles.count(),
         "icon": "bi-check-circle", "text_color": "text-success"},
        {"title": "Checked Out", "value": signed_out_vehicles.count(),
         "icon": "bi-box-arrow-right", "text_color": "text-dark"},
    ]

    return render(request, "vehicle/dashboard.html", {
        "cards": cards,
        "parked_vehicles": parked_vehicles,
        "signed_out_vehicles": signed_out_vehicles,
    })


def checkout_vehicle(request, pk):
    if not request.user.is_authenticated or request.user.role != "ATTENDANT":
        return no_access()

    vehicle = get_object_or_404(Registration, id=pk)

    now = timezone.now()
    duration = (now - vehicle.arrival_time).total_seconds() / 3600

    category = vehicle.vehicle_type

    if duration < 3:
        fee = category.short_stay_rate
        rate_type = "short"

    else:
        arrival_hour = timezone.localtime(vehicle.arrival_time).hour

        if 6 <= arrival_hour < 19:
            fee = category.day_rate
            rate_type = "day"
        else:
            fee = category.night_rate
            rate_type = "night"

    if request.method == "POST":
        form = CheckOutForm(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)

            vehicle.departure_time = now
            vehicle.fee = fee
            vehicle.rate_type = rate_type
            vehicle.status = "signed_out"

            vehicle.save()

            messages.success(request, "Vehicle checked out successfully.")
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

# RECEIPT

def vehicle_receipt(request, pk):
    if not request.user.is_authenticated or request.user.role not in ["ADMIN", "ATTENDANT"]:
        return no_access()

    vehicle = get_object_or_404(Registration, id=pk)

    if vehicle.departure_time and vehicle.arrival_time:
        duration = (vehicle.departure_time - vehicle.arrival_time).total_seconds() / 3600
    else:
        duration = 0

    return render(request, "receipt.html", {
        "vehicle": vehicle,
        "hours": round(duration, 2),
        "fee": vehicle.fee,
        "rate_type": vehicle.rate_type or "pending"
    })

# EDIT VEHICLE

def edit_vehicle(request, id):
    if not request.user.is_authenticated or request.user.role != "ATTENDANT":
        return no_access()

    vehicle = get_object_or_404(Registration, id=id)

    if vehicle.status != "parked":
        messages.error(request, "You cannot edit a signed-out vehicle.")
        return redirect("dashboard")

    form = RegistrationForm(request.POST or None, instance=vehicle)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle updated successfully.")
            return redirect("dashboard")

    return render(request, "vehicle/edit_vehicle.html", {"form": form})