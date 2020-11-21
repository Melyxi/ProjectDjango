from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, reverse
from basketapp.models import Basket
from mainapp.models import Product
from django.contrib.auth.decorators import login_required
import random
from django.template.loader import render_to_string
from django.http import JsonResponse


def auth_user_basket(request):
    user = request.user
    if user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).select_related('product')
        return basket
    else:
        return []



@login_required
def basket(request):
    basket = auth_user_basket(request).order_by('product__category')

    content = {'basket':basket}
    return render(request, 'basketapp/basket.html', content)

@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    product = get_object_or_404(Product, pk=pk)

    print(Product.objects.filter(pk=pk))
    basket = Basket.objects.filter(user=request.user, product=product).select_related('product').first()
    
    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))
        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user). \
            order_by('product__category').select_related('product')

        content = {
            'basket': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', content)
        print(result, 'fsfsdf')
        return JsonResponse({'result': result})