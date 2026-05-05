# from django.shortcuts import render, redirect, get_object_or_404
# from django.utils import timezone
# from django.contrib import messages
# from django.db.models import Q
# from django.http import HttpResponseForbidden
# from vehicle.forms import CategoryForm, RegistrationForm, CheckOutForm
# from .models import Category, Registration


# # def no_access():
# #     # Returns a forbidden response when user has no permission
# #     return HttpResponseForbidden("You do not have permission to access this page.")

# def no_access(request):
#     messages.error(request, "You are not authorized to access this page.")
#     return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


# def vehicle_category(request):
#     if not request.user.is_authenticated or request.user.role != "ADMIN":
#         return no_access(request)

#     form = CategoryForm()

#     if request.method == "POST":
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Category added successfully.")
#             return redirect("vehicle_category_list")

#     return render(request, "category/add_category.html", {"form": form})


# def vehicle_category_list(request):
#     if not request.user.is_authenticated or request.user.role not in ["ADMIN", "ATTENDANT"]:
#         return no_access(request)

#     categories = Category.objects.all()
#     return render(request, "category/category_list.html", {"categories": categories})


# def edit_category(request, id):
#     if not request.user.is_authenticated or request.user.role != "ADMIN":
#         return no_access(request)

#     category = get_object_or_404(Category, id=id)
#     form = CategoryForm(request.POST or None, instance=category)

#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Category updated successfully.")
#             return redirect("vehicle_category_list")

#     return render(request, "category/edit_category.html", {"form": form})


# def delete_category(request, id):
#     if not request.user.is_authenticated or request.user.role != "ADMIN":
#         return no_access(request)

#     category = get_object_or_404(Category, id=id)

#     if request.method == "POST":
#         category.delete()
#         messages.success(request, "Category deleted successfully.")
#         return redirect("vehicle_category_list")

#     return render(request, "category/delete_category.html", {"category": category})


# # VEHICLE REGISTRATION

# def register_vehicle(request):
#     if not request.user.is_authenticated or request.user.role != "ATTENDANT":
#         return no_access(request)

#     form = RegistrationForm()

#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             vehicle = form.save(commit=False)

#             vehicle.arrival_time = timezone.now()
#             vehicle.status = "parked"
#             vehicle.registered_by = request.user
#             vehicle.save()

#             messages.success(request, "Vehicle registered successfully.")
#             return redirect("dashboard")

#     return render(request, "vehicle/register_vehicle.html", {"form": form})



# # DASHBOARD

# def dashboard(request):
#     if not request.user.is_authenticated or request.user.role not in ["ADMIN", "ATTENDANT"]:
#         return no_access(request)
    
#     query = request.GET.get('q', '').strip()

#     all_vehicles = Registration.objects.all().order_by("-arrival_time")
#     # search query
#     if query:
#         all_vehicles = all_vehicles.filter( Q(plate_number__icontains=query))

#     parked_vehicles = all_vehicles.filter(status="parked")
#     signed_out_vehicles = all_vehicles.filter(status="signed_out")

#     cards = [
#         {"title": "Total Vehicles", "value": all_vehicles.count(),
#          "icon": "bi-car-front", "text_color": "text-primary"},
#         {"title": "Currently Parked", "value": parked_vehicles.count(),
#          "icon": "bi-check-circle", "text_color": "text-success"},
#         {"title": "Checked Out", "value": signed_out_vehicles.count(),
#          "icon": "bi-box-arrow-right", "text_color": "text-dark"},
#     ]

#     return render(request, "vehicle/dashboard.html", {
#         "cards": cards,
#         "parked_vehicles": parked_vehicles,
#         "signed_out_vehicles": signed_out_vehicles,
#     })


# def checkout_vehicle(request, pk):
#     if not request.user.is_authenticated or request.user.role != "ATTENDANT":
#         return no_access(request)

#     vehicle = get_object_or_404(Registration, id=pk)

#     now = timezone.now()
#     duration = (now - vehicle.arrival_time).total_seconds() / 3600

#     category = vehicle.vehicle_type

#     if duration < 3:
#         fee = category.short_stay_rate
#         rate_type = "short"

#     else:
#         arrival_hour = timezone.localtime(vehicle.arrival_time).hour

#         if 6 <= arrival_hour < 19:
#             fee = category.day_rate
#             rate_type = "day"
#         else:
#             fee = category.night_rate
#             rate_type = "night"

#     if request.method == "POST":
#         form = CheckOutForm(request.POST, instance=vehicle)
#         if form.is_valid():
#             vehicle = form.save(commit=False)

#             vehicle.departure_time = now
#             vehicle.fee = fee
#             vehicle.rate_type = rate_type
#             vehicle.status = "signed_out"

#             vehicle.save()

#             messages.success(request, "Vehicle checked out successfully.")
#             return redirect("dashboard")
#     else:
#         form = CheckOutForm(instance=vehicle)

#     return render(request, "vehicle/exit.html", {
#         "vehicle": vehicle,
#         "form": form,
#         "duration": round(duration, 2),
#         "fee": fee,
#         "rate_type": rate_type
#     })

# # RECEIPT

# def vehicle_receipt(request, pk):
#     if not request.user.is_authenticated or request.user.role not in ["ADMIN", "ATTENDANT"]:
#         return no_access(request)

#     vehicle = get_object_or_404(Registration, id=pk)

#     if vehicle.departure_time and vehicle.arrival_time:
#         duration = (vehicle.departure_time - vehicle.arrival_time).total_seconds() / 3600
#     else:
#         duration = 0

#     return render(request, "receipt.html", {
#         "vehicle": vehicle,
#         "hours": round(duration, 2),
#         "fee": vehicle.fee,
#         "rate_type": vehicle.rate_type or "pending"
#     })

# # EDIT VEHICLE

# def edit_vehicle(request, id):
#     if not request.user.is_authenticated or request.user.role != "ATTENDANT":
#         return no_access(request)

#     vehicle = get_object_or_404(Registration, id=id)

#     if vehicle.status != "parked":
#         messages.error(request, "You cannot edit a signed-out vehicle.")
#         return redirect("dashboard")

#     form = RegistrationForm(request.POST or None, instance=vehicle)

#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Vehicle updated successfully.")
#             return redirect("dashboard")

#     return render(request, "vehicle/edit_vehicle.html", {"form": form})


from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from vehicle.forms import CategoryForm, RegistrationForm, CheckOutForm
from .models import Category, Registration


# =========================
# ACCESS CONTROL (NO REDIRECT VERSION)
# =========================

def no_access(request, template, context=None):
    messages.error(request, "You are not authorized to access this page.")
    return render(request, template, context or {})


# =========================
# CATEGORY
# =========================

@login_required
def vehicle_category(request):
    if request.user.role != "ADMIN":
        return no_access(request, "category/add_category.html", {
            "form": CategoryForm()
        })

    form = CategoryForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category added successfully.")
        return redirect("vehicle_category_list")

    return render(request, "category/add_category.html", {"form": form})


@login_required
def vehicle_category_list(request):
    if request.user.role not in ["ADMIN", "ATTENDANT"]:
        return no_access(request, "category/category_list.html")

    categories = Category.objects.all()
    return render(request, "category/category_list.html", {"categories": categories})


@login_required
def edit_category(request, id):
    if request.user.role != "ADMIN":
        category = get_object_or_404(Category, id=id)
        return no_access(request, "category/edit_category.html", {
            "form": CategoryForm(instance=category)
        })

    category = get_object_or_404(Category, id=id)
    form = CategoryForm(request.POST or None, instance=category)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category updated successfully.")
        return redirect("vehicle_category_list")

    return render(request, "category/edit_category.html", {"form": form})


@login_required
def delete_category(request, id):
    if request.user.role != "ADMIN":
        category = get_object_or_404(Category, id=id)
        return no_access(request, "category/delete_category.html", {
            "category": category
        })

    category = get_object_or_404(Category, id=id)

    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect("vehicle_category_list")

    return render(request, "category/delete_category.html", {"category": category})


# =========================
# VEHICLE REGISTRATION
# =========================

@login_required
def register_vehicle(request):
    if request.user.role != "ATTENDANT":
        return no_access(request, "vehicle/register_vehicle.html", {
            "form": RegistrationForm()
        })

    form = RegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        vehicle = form.save(commit=False)
        vehicle.arrival_time = timezone.now()
        vehicle.status = "parked"
        vehicle.registered_by = request.user
        vehicle.save()

        messages.success(request, "Vehicle registered successfully.")
        return redirect("dashboard")

    return render(request, "vehicle/register_vehicle.html", {"form": form})


# =========================
# DASHBOARD
# =========================

@login_required
def dashboard(request):
    if request.user.role not in ["ADMIN", "ATTENDANT"]:
        return no_access(request, "vehicle/dashboard.html")

    query = request.GET.get('q', '').strip()

    all_vehicles = Registration.objects.all().order_by("-arrival_time")

    if query:
        all_vehicles = all_vehicles.filter(
            Q(plate_number__icontains=query)
        )

    parked_vehicles = all_vehicles.filter(status="parked")
    signed_out_vehicles = all_vehicles.filter(status="signed_out")

    cards = [
        {
            "title": "Total Vehicles",
            "value": all_vehicles.count(),
            "icon": "bi-car-front",
            "text_color": "text-primary",
        },
        {
            "title": "Currently Parked",
            "value": parked_vehicles.count(),
            "icon": "bi-check-circle",
            "text_color": "text-success",
        },
        {
            "title": "Checked Out",
            "value": signed_out_vehicles.count(),
            "icon": "bi-box-arrow-right",
            "text_color": "text-dark",
        },
    ]

    return render(request, "vehicle/dashboard.html", {
        "cards": cards,
        "parked_vehicles": parked_vehicles,
        "signed_out_vehicles": signed_out_vehicles,
    })


# =========================
# CHECKOUT
# =========================

@login_required
def checkout_vehicle(request, pk):
    if request.user.role != "ATTENDANT":
        return no_access(request, "vehicle/exit.html", {
            "form": CheckOutForm()
        })

    vehicle = get_object_or_404(Registration, id=pk)

    if request.method == "POST":
        form = CheckOutForm(request.POST, instance=vehicle)
        if form.is_valid():
            vehicle = form.save(commit=False)

            vehicle.departure_time = timezone.now()

            fee, rate_type = vehicle.calculate_fee()

            vehicle.fee = fee
            vehicle.rate_type = rate_type
            vehicle.status = "signed_out"

            vehicle.save()

            messages.success(request, "Vehicle checked out successfully.")
            return redirect("dashboard")
    else:
        form = CheckOutForm(instance=vehicle)

    fee, rate_type = vehicle.calculate_fee()
    duration = (timezone.now() - vehicle.arrival_time).total_seconds() / 3600

    return render(request, "vehicle/exit.html", {
        "vehicle": vehicle,
        "form": form,
        "duration": round(duration, 2),
        "fee": fee,
        "rate_type": rate_type
    })


# =========================
# RECEIPT
# =========================

@login_required
def vehicle_receipt(request, pk):
    if request.user.role not in ["ADMIN", "ATTENDANT"]:
        return no_access(request, "receipt.html")

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


# =========================
# EDIT VEHICLE
# =========================

@login_required
def edit_vehicle(request, id):
    if request.user.role != "ATTENDANT":
        vehicle = get_object_or_404(Registration, id=id)
        return no_access(request, "vehicle/edit_vehicle.html", {
            "form": RegistrationForm(instance=vehicle)
        })

    vehicle = get_object_or_404(Registration, id=id)

    if vehicle.status != "parked":
        messages.error(request, "You cannot edit a signed-out vehicle.")
        return redirect("dashboard")

    form = RegistrationForm(request.POST or None, instance=vehicle)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Vehicle updated successfully.")
        return redirect("dashboard")

    return render(request, "vehicle/edit_vehicle.html", {"form": form})