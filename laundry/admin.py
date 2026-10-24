from django.contrib import admin
from django.contrib import admin
from .models import (
    Customer,
    Service,
    LaundryOrder,
    Payment,
    Employee,
    BusinessInformation,
)

admin.site.register(Customer)
admin.site.register(Service)
admin.site.register(LaundryOrder)
admin.site.register(Payment)
admin.site.register(Employee)
admin.site.register(BusinessInformation)

# Register your models here.
