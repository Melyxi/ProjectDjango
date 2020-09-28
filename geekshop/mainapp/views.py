from django.shortcuts import render
from .models import Product, ProductCategory
# Create your views here.


def main(request):
    list_game = Product.objects.all()[:4]
    content = {
        'games': list_game
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    print(request.GET)
    list_game = Product.objects.all()[:4]
    list_categories = ProductCategory.objects.all()
    content = {
        'games': list_game,
        'categories': list_categories
    }
    return render(request, 'mainapp/products.html', content)


def product(request):
    list_game = Product.objects.all()

    print(list_game)
    content = {
        'games': list_game

    }

    return render(request, 'mainapp/product.html', content)