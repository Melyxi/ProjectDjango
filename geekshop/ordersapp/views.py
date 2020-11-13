from django.http import JsonResponse
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.http import JsonResponse
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from mainapp.models import Product
from basketapp.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm, AjaxFormMixin
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(ListView, self).dispatch(*args, **kwargs)


class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_queryset(self):
        return super(OrderItemsCreate, self).get_queryset().select_related('product')

    def get_context_data(self, **kwargs):
        data = super(OrderItemsCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.get_items(self.request.user)

            if len(basket_items):

                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()

                for num, form in enumerate(formset.forms):
                   form.initial['product'] = basket_items[num].product
                   form.initial['quantity'] = basket_items[num].quantity
                   form.initial['price'] = basket_items[num].product.price
               # basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
       context = self.get_context_data()
       orderitems = context['orderitems']

       with transaction.atomic():
           Basket.get_items(self.request.user).delete()
           form.instance.user = self.request.user
           self.object = form.save()
           if orderitems.is_valid():
               orderitems.instance = self.object
               orderitems.save()

       # удаляем пустой заказ
       if self.object.get_total_cost() == 0:
           self.object.delete()

       return super(OrderItemsCreate, self).form_valid(form)

class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:orders_list')

    def get_queryset(self):
        return super(OrderItemsUpdate, self).get_queryset()



    def get_context_data(self, **kwargs):
        data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
        print(data)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        print(self.request.POST)

        # if self.request.is_ajax():
        #     if self.request.POST:
        #         print('post')
        #         data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        #
        #
        #
        #
        #     else:
        #         print('nopost')
        #         formset = OrderFormSet(instance=self.object)
        #         for form in formset.forms:
        #             if form.instance.pk:
        #                 form.initial['price'] = form.instance.product.price
        #             data['orderitems'] = formset
        #


        if self.request.POST:

            print('post')
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
            # print(data['orderitems'])
        else:
            queryset = self.object.orderitems.select_related()
            formset = OrderFormSet(instance=self.object, queryset=queryset)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
                data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        self.object = form.save()
        if orderitems.is_valid():
           orderitems.instance = self.object
           orderitems.save()

        # удаляем пустой заказ
        if self.object.get_total_cost() == 0:
           self.object.delete()

        print(form)

        return super(OrderItemsUpdate, self).form_valid(form)



def order_ajax(request, pk):

    print('order_ajax')
    OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

    obj = Order.objects.filter(pk=pk).first()
    print(obj)
    if request.is_ajax():
        # if OrderFormSet.is_valid():
        #     OrderFormSet.save()

        print(OrderFormSet(instance=obj))
        print('ajax done')
        print(request.POST)


        if request.POST:
            data = OrderFormSet(request.POST, instance=obj)
            data.save()
            print(data)
        else:
            data = OrderFormSet()


        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_product_price(request, pk):
   if request.is_ajax():
       product = Product.objects.filter(pk=int(pk)).first()
       if product:
           return JsonResponse({'price': product.price})
       else:
           return JsonResponse({'price': 0})





class OrderDelete(DeleteView):
    model = Order

    success_url = reverse_lazy('ordersapp:orders_list')


class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
       context = super(OrderRead, self).get_context_data(**kwargs)
       context['title'] = 'заказ/просмотр'
       return context

def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))

@receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    if update_fields is ('quantity' or 'product'):
        if instance.pk:
            instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
        else:
            instance.product.quantity -= instance.quantity
        instance.product.save()

@receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
   instance.product.quantity += instance.quantity
   instance.product.save()