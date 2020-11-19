from django import forms
from django.core.exceptions import ValidationError
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
    #error = forms.CharField(max_length=400, label='цена', required=False)

    def __init__(self, *args, **kwargs):

        super(OrderItemForm, self).__init__(*args, **kwargs)


        for field_name, field in self.fields.items():
            # print(field_name, field, "поля")
            # print(self.instance.pk)
            if self.instance.pk:
                self.fields['quantity'].widget.attrs['max'] = self.instance.quantity + self.instance.product.quantity
            self.fields['product'].queryset = Product.get_items().select_related()
            field.widget.attrs['class'] = 'form-control'


        #print(old_form, 'old_form')
        # print(self.instance.get_item(157))
        # r = OrderItem.objects.filter(pk=self.instance.pk).first()
        # print(r)

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data, 'clean_data')
        # print(self.instance.quantity, 'instance q')
        # print(self.instance.pk, 'instance pk')

        post_quantity = self.instance.quantity
        if 'product' in cleaned_data:
            if cleaned_data['quantity'] - post_quantity > cleaned_data['product'].quantity:
                cleaned_data['quantity'] = cleaned_data['product'].quantity

            if cleaned_data['quantity'] == 0:
                cleaned_data['quantity'] = post_quantity
                cleaned_data['DELETE'] = True
                print(cleaned_data)

        return cleaned_data

    # def is_valid(self):
    #
    #     valid = super(OrderItemForm, self).is_valid()
    #     if not valid:
    #         return valid
    #     if self.message_error:
    #         return False
    #     else:
    #         return True

class AjaxFormMixin(FormView):
    class AjaxFormMixin(FormView):
        template_name = 'order_form.html'

        def form_valid(self, form):
            form.save()
            return HttpResponse('OK')

        def form_invalid(self, form):
            errors_dict = json.dumps(dict([(k, [e for e in v]) for k, v in form.errors.items()]))
            return HttpResponseBadRequest(json.dumps(errors_dict))