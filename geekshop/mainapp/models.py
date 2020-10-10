from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=60, verbose_name="имя", unique=True)
    descriotion = models.TextField(verbose_name="описание", blank=True)

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

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Gallery(models.Model):
    name_gallery = models.ForeignKey(Product, on_delete=models.CASCADE)
    hot_image =  models.ImageField(upload_to="hot_images", blank=True)
    image_product = models.ImageField(upload_to="image_product", blank=True)