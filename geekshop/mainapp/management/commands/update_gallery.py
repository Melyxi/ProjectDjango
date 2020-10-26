from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product, Gallery
from django.contrib.auth.models import User

import json, os

class Command(BaseCommand):
    def handle(self, *args, **options):
        products = Product.objects.all()
        for product in products:
            product_gallery = Gallery.objects.create(name_gallery=product)
            product_gallery.save()

