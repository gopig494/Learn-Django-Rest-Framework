from django.contrib import admin
from RestSApi.models import Customer,City

class FetchCustomer(admin.ModelAdmin):
    data = ["name","age","address","phone"]

admin.site.register(Customer,FetchCustomer)
admin.site.register(City)