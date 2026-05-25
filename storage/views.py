from django.shortcuts import render, redirect, get_object_or_404
from .models import MembraneBox, Location, MembraneType, StorageActivityLog

def home(request):
    stored = MembraneBox.objects.filter(status="STORED")
    in_use = MembraneBox.objects.filter(status="IN_USE")
    consumed = MembraneBox.objects.filter(status="CONSUMED")

    return render(request, "home.html", {
        "stored": stored,
        "in_use": in_use,
        "consumed": consumed,
        "stored_count": stored.count(),
        "in_use_count": in_use.count(),
        "consumed_count": consumed.count(),
    })


def add_box(request):
    if request.method == "POST":
        barcode = request.POST.get("barcode")
        type_id = request.POST.get("type_id")
        location_id = request.POST.get("location_id")

        # Validation – check all fields exist
        if not barcode or not type_id or not location_id:
            return render(request, "add_box.html", {
                "types": MembraneType.objects.all(),
                "locations": Location.objects.all(),
                "error": "All fields are required. Make sure membrane types and locations exist."
            })

        membrane_type = MembraneType.objects.get(id=type_id)
        location = Location.objects.get(id=location_id)

        box = MembraneBox.objects.create(
            barcode=barcode,
            membrane_type=membrane_type,
            location=location,
            status="STORED"
        )

        StorageActivityLog.objects.create(
            box=box,
            action="STORED"
        )

        return redirect("home")

    return render(request, "add_box.html", {
        "types": MembraneType.objects.all(),
        "locations": Location.objects.all()
    })


def move_to_in_use(request):
    if request.method == "POST":
        barcode = request.POST["barcode"]
        box = get_object_or_404(MembraneBox, barcode=barcode)

        box.status = "IN_USE"
        box.location = None
        box.save()

        StorageActivityLog.objects.create(
            box=box,
            action="IN_USE"
        )

        return redirect("home")

    return render(request, "move_in_use.html")


def consume_box(request):
    if request.method == "POST":
        barcode = request.POST["barcode"]
        box = get_object_or_404(MembraneBox, barcode=barcode)

        box.status = "CONSUMED"
        box.location = None
        box.save()

        StorageActivityLog.objects.create(
            box=box,
            action="CONSUMED"
        )

        return redirect("home")

    return render(request, "consume_box.html")