from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductCategory, Gallery
from basketapp.models import Basket
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page

def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)

def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)

def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')

def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products = get_products()

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
    list_game = get_products()[:4]
    content = {
        'games': list_game,
        "title": title,

    }
    return render(request, 'mainapp/index.html', content)

@cache_page(1600)
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
            category = get_category(pk)
            print("+++")
            list_game = get_products_in_category_orederd_by_price(pk)

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

@cache_page(1600)
def product(request, pk):
    prod = get_product(pk)
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