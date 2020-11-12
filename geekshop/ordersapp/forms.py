from django import forms
from ordersapp.models import Order, OrderItem
from django.views.generic import FormView
from django.shortcuts import HttpResponse
import json
from django.http import HttpResponseBadRequest
from mainapp.models import Product

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
           field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        exclude = ()

    price = forms.CharField(label='цена', required=False)

    def __init__(self, *args, **kwargs):

        #self.fields['product'].queryset = Product.get_items()
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
           field.widget.attrs['class'] = 'form-control'


class AjaxFormMixin(FormView):
    class AjaxFormMixin(FormView):
        template_name = 'order_form.html'

        def form_valid(self, form):
            form.save()
            return HttpResponse('OK')

        def form_invalid(self, form):
            errors_dict = json.dumps(dict([(k, [e for e in v]) for k, v in form.errors.items()]))
            return HttpResponseBadRequest(json.dumps(errors_dict))