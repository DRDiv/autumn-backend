from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Event)
admin.site.register(Amenity)
admin.site.register(AmenitySlot)
admin.site.register(Request)
admin.site.register(Team)
admin.site.register(Booking)

