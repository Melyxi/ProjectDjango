from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory
# Create your views here.


def main(request):
    title = 'главная'
    list_game = Product.objects.all()[:4]
    content = {
        'games': list_game,
        "title": title
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    title = 'галерея'
    print(pk)

    list_categories = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            list_game = Product.objects.all().order_by('price')
            category = 'все'
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            print("+++")
            list_game = Product.objects.filter(category__pk=pk)

        content = {
            'games': list_game,
            'categories': list_categories,
            "title": title,
            'pk_category': category
        }
        return render(request, 'mainapp/products_list.html', content)

    same_game = Product.objects.all()[1:4]
    content = {
        'games': same_game,
        'categories': list_categories,
        "title": title
    }

    return render(request, 'mainapp/products.html', content)


def product(request):
    title = 'продукт'
    list_game = Product.objects.all()

    print(list_game)
    content = {
        'games': list_game,
        "title": title

    }

    return render(request, 'mainapp/product.html', content)