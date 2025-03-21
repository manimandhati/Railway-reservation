from django.contrib import admin

from .models import trains,Books,payment

# Register your models here.

admin.site.register(trains)
admin.site.register(Books)
admin.site.register(payment)