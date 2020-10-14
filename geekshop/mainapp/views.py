from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory, Gallery
from basketapp.models import Basket
import random


def basket_item(request):

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
        return basket
    else:
        return []


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 2)[:2]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category). \
                        exclude(pk=hot_product.pk)[:3]

    return same_products

def hot_gallery(hot_game):
    hot_gallery = []
    for i in hot_game:
        print(i.name)
        image = Gallery.objects.filter(name_gallery=i.pk)
        print(hot_gallery.append(list(image)))
    return hot_gallery


def main(request):
    basket = basket_item(request)

    title = 'главная'
    list_game = Product.objects.all()[:4]
    content = {
        'games': list_game,
        "title": title,
        'basket': basket,
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    title = 'галерея'
    print(pk)
    basket = basket_item(request)
    list_categories = ProductCategory.objects.all()
    print(list_categories)
    hot_game = get_hot_product()
    hot_image = hot_gallery(hot_game)
    print(hot_image)
    print('-----')

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
            'pk_category': category,
            'basket': basket,
        }
        return render(request, 'mainapp/products_list.html', content)

    same_game = Product.objects.all()[1:4]

    content = {
        'games': same_game,
        'categories': list_categories,
        "title": title,
        'basket': basket,
        'hot_image': hot_image,

    }

    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    prod = Product.objects.filter(pk=pk).first()
    same_product = get_same_products(prod)
    print(same_product)
    title = 'продукты'
    img_gallery = Gallery.objects.filter(name_gallery=pk)
    # print(img_gallery[0].name_gallery, 'fdsfdsafa')
    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': basket_item(request),
        'img_gallery': img_gallery,
        'same_product': same_product
    }
    return render(request, 'mainapp/product.html', content)