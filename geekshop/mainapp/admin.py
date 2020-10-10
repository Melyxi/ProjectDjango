from django.contrib import admin

# Register your models here.
from .models import ProductCategory, Product, Gallery

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(Gallery)