from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'age')
admin.site.register(Customer, CustomerAdmin)

