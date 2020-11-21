from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategory
from django.core.management import call_command
from django.test import TestCase
from mainapp.models import Product, ProductCategory


class TestMainappSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        # call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/category/0/')
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="гонки")
        self.product_1 = Product.objects.create(name="формула 1",
                                                category=category,
                                                price=20,
                                                quantity=150)

        self.product_2 = Product.objects.create(name="ралли 1",
                                                category=category,
                                                price=30,
                                                quantity=125,
                                                is_active=False)

        self.product_3 = Product.objects.create(name="ралли 2",
                                                category=category,
                                                price=34,
                                                quantity=115)

    def test_product_get(self):
        product_1 = Product.objects.get(name="формула 1")
        product_2 = Product.objects.get(name="ралли 1")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="формула 1")
        product_2 = Product.objects.get(name="ралли 1")
        self.assertEqual(str(product_1), 'формула 1 (гонки)')
        self.assertEqual(str(product_2), 'ралли 1 (гонки)')

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="формула 1")
        product_3 = Product.objects.get(name="ралли 2")
        products = product_1.get_items()
        print(products)
        # self.assertEqual(list(products), [product_1, product_3])
