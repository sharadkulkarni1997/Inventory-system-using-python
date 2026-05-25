from django.db import models

class MembraneType(models.Model):
    name = models.CharField(max_length=100)
    membranes_per_box = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.membranes_per_box}/box)"


class Location(models.Model):
    label = models.CharField(max_length=20, unique=True)
    capacity = models.IntegerField(default=2)

    def __str__(self):
        return self.label


class MembraneBox(models.Model):
    STATUS_CHOICES = [
        ("STORED", "Stored"),
        ("IN_USE", "In Use"),
        ("CONSUMED", "Consumed"),
    ]

    barcode = models.CharField(max_length=100, unique=True)
    membrane_type = models.ForeignKey(MembraneType, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="STORED")
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.barcode} - {self.status}"


class StorageActivityLog(models.Model):
    box = models.ForeignKey(MembraneBox, on_delete=models.CASCADE)
    action = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.box.barcode} - {self.action} @ {self.timestamp}"