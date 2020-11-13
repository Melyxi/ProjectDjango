from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProductCategory(models.Model):
    name = models.CharField(max_length=60, verbose_name="имя", unique=True)
    descriotion = models.TextField(verbose_name="описание", blank=True)
    is_active = models.BooleanField(verbose_name='активна', db_index=True, default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="имя продукта")
    image = models.ImageField(upload_to="product_images", blank=True)
    short_desc = models.CharField(max_length=120, verbose_name="краткое описание продукта", blank=True)
    descriotion = models.TextField(verbose_name="описание продукта", blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="цена")
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)
    is_active = models.BooleanField(verbose_name='активна', default=True, db_index=True)

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Gallery(models.Model):
    name_gallery = models.OneToOneField(Product, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    hot_image = models.ImageField(upload_to="hot_images", blank=True)
    image_product = models.ImageField(upload_to="image_product", blank=True)

    @receiver(post_save, sender=Product)
    def create_gallery(sender, instance, created, **kwargs):
        if created:
            print('create')
            print(instance)

            Gallery.objects.create(name_gallery=instance)

    @receiver(post_save, sender=Product)
    def save_gallery(sender, instance, **kwargs):
        print(kwargs)

        print('save')
        instance.gallery.save()
