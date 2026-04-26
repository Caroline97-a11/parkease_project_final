from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Tyre, Battery
from .forms import ServiceForm, TyreAddForm, BatteryAddForm
from django.contrib import messages


# service price logic
def add_service_price(request):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    form = ServiceForm()

    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("service_price_list")

    return render(request, "price/add_price.html", {"form": form})


def service_price_list(request):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    prices = Service.objects.all()
    return render(request, "price/price_list.html", {"prices": prices})


def edit_price(request, id):
    price = get_object_or_404(Service, id=id)

    if request.method == "POST":
        form = ServiceForm(request.POST, instance=price)
        if form.is_valid():
            form.save()
            messages.success(request, "Price updated successfully.")
            return redirect('service_price_list')
    else:
        form = ServiceForm(instance=price)

    return render(request, 'price/edit_price.html', {'form': form})

def delete_price(request, id):
    price = get_object_or_404(Service, id=id)

    if request.method == "POST":
        price.delete()
        messages.success(request, "Price deleted successfully.")
        return redirect('service_price_list')

    return render(request, 'price/delete_price.html', {'price': price})


#tyre service logic
def add_tyre_service(request):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    form = TyreAddForm()

    if request.method == "POST":
        form = TyreAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tyre_list')

    return render(request, "tyre/add_tyre.html", {"form": form})


def tyre_list(request):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    services = Tyre.objects.all().order_by("-date")
    return render(request, "tyre/tyre_list.html", {"services": services})

def tyre_detail(request, id):
    tyre = get_object_or_404(Tyre, id=id)
    return render(request, 'tyre/tyre_detail.html', {'tyre': tyre})

def edit_tyre(request, id):
    tyre = get_object_or_404(Tyre, id=id)

    if request.method == "POST":
        form = TyreAddForm(request.POST, instance=tyre)
        if form.is_valid():
            form.save()
            messages.success(request, "Tyre service updated successfully.")
            return redirect('tyre_detail', id=tyre.id)
    else:
        form = TyreAddForm(instance=tyre)

    return render(request, 'edit_tyre.html', {'form': form})

def delete_tyre(request, id):
    tyre = get_object_or_404(Tyre, id=id)

    if request.method == "POST":
        tyre.delete()
        messages.success(request, "Tyre service deleted.")
        return redirect('tyre_list')

    return render(request, 'tyre/delete_tyre.html', {'tyre': tyre})

def tyre_receipt(request, pk):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    service = get_object_or_404(Tyre, id=pk)
    price = service.service.price

    return render(request, "tyre_receipt.html", {
        "service": service,
        "price": price
    })


# bettery service logic
def add_battery_service(request):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })
    form = BatteryAddForm()

    if request.method == "POST":
        form = BatteryAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("battery_list")

    return render(request, "battery/add_battery.html", {"form": form})


def battery_list(request):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    batteries = BatteryAddForm.objects.all().order_by("-date")
    return render(request, "battery/battery_list.html", {"batteries": batteries})

def battery_receipt(request, pk):

    if request.user.role != "MANAGER":
        return render(request, "403.html", {
            "message": "You have no access to this page"
        })

    service = get_object_or_404(Battery, id=pk)

    return render(request, "battery/battery_receipt.html", {
        "service": service,
        "price": service.price
    })


def battery_detail(request, id):
    battery = get_object_or_404(Battery, id=id)
    return render(request, 'battery/battery_detail.html', {'battery': battery})


def edit_battery(request, id):
    battery = get_object_or_404(Battery, id=id)

    if request.method == "POST":
        form = BatteryAddForm(request.POST, instance=battery)
        if form.is_valid():
            form.save()
            messages.success(request, "Battery service updated successfully.")
            return redirect('battery_list')  
    else:
        form = BatteryAddForm(instance=battery)

    return render(request, 'battery/edit_battery.html', {'form': form})


def delete_battery(request, id):
    battery = get_object_or_404(Battery, id=id)

    if request.method == "POST":
        battery.delete()
        messages.success(request, "Battery service deleted successfully.")
        return redirect('battery_list')

    return render(request, 'battery/delete_battery.html', {'battery': battery})