from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductCategory, Gallery
from basketapp.models import Basket
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

def get_hot_product():
    products = Product.objects.filter(is_active=True)

    return random.sample(list(products), 2)[:2]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).filter(is_active=True).exclude(pk=hot_product.pk).select_related('category')[:3]

    return same_products

def hot_gallery(hot_game):
    hot_gallery = []
    for i in hot_game:
        print(i.name)
        image = Gallery.objects.filter(name_gallery=i.pk).select_related('name_gallery')
        print(hot_gallery.append(list(image)))
    return hot_gallery


def main(request):


    title = 'главная'
    list_game = Product.objects.all()[:4]
    content = {
        'games': list_game,
        "title": title,

    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None, page=1):

    if not request.session.get("count", False): # сделал количество товара на странице с помощью сессии
                                                # как правильно удалить из сессии?
        count_product = 5
    else:
        count_product = request.session["count"]
    try:
        count_product = int(request.GET['count_product'])
        request.session["count"] = count_product
    except KeyError:
        pass

    print(request.session.items(), "session")
    title = 'галерея'
    list_categories = ProductCategory.objects.all()
    # hot_game = get_hot_product()
    # hot_image = hot_gallery(hot_game)
    #hot_image=[1,2]



    if pk is not None:
        if pk == 0:
            list_game = Product.objects.filter(is_active=True, category__is_active=True).order_by('price').select_related('category')
            category = {'name':'все', 'pk': 0}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            print("+++")
            list_game = Product.objects.filter(category__pk=pk).filter(is_active=True, category__is_active=True).order_by('price').select_related('category')

        paginator = Paginator(list_game, count_product)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
                'games': list_game,
                'categories': list_categories,
                "title": title,
                'pk_category': category,
                'products': products_paginator,

        }
        return render(request, 'mainapp/products_list.html', content)

    same_game = Product.objects.all()[1:4]

    content = {
        'games': same_game,
        'categories': list_categories,
        "title": title,
        #'hot_image': hot_image,

    }

    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    prod = Product.objects.filter(pk=pk).first()
    same_product = get_same_products(prod)
    print(same_product)
    title = 'продукты'
    img_gallery = Gallery.objects.filter(name_gallery=pk).select_related('name_gallery')
    # print(img_gallery[0].name_gallery, 'fdsfdsafa')
    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'img_gallery': img_gallery,
        'same_product': same_product
    }
    return render(request, 'mainapp/product.html', content)