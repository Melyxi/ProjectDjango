from basketapp.models import Basket


def basket(request):
   print(f'context processor basket works')
   basket = []
   if request.user.is_authenticated:

       basket = request.user.basket.select_related()
   return {
       'basket': basket,
   }