from django.contrib import admin
from .models import Product,Claim, Warranty, ExtendedWarranty
# Register your models here.
admin.site.register(Product)
admin.site.register(Claim)
admin.site.register(Warranty)
admin.site.register(ExtendedWarranty)