from django.contrib import admin
from .models import MembraneType, Location, MembraneBox, StorageActivityLog

admin.site.register(MembraneType)
admin.site.register(Location)
admin.site.register(MembraneBox)
admin.site.register(StorageActivityLog)