from django.db import transaction
from django.db.models import F
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, reverse
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory, Gallery
from django.contrib.auth.decorators import user_passes_test
from authapp.forms import ShopUserRegisterForm
from .forms import ShopUserAdminEditForm, ProductCategoryEditForm, GalleryEditForm, ProductEditForm
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from authapp.forms import ShopUserEditForm, AdminUserEditForm
from django.views.generic.detail import DetailView
from ordersapp.models import Order
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection


class UsersListView(ListView):
    model=ShopUser
    template_name = 'adminapp/users.html'
    paginate_by = 4

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context

    def get_ordering(self):
        return '-is_active', '-is_superuser', '-is_staff', 'username'

    # def get_paginator(self, queryset, per_page, orphans=0,
    #                   allow_empty_first_page=True, **kwargs):
    #     """Return an instance of the paginator for this view."""
    #     return self.paginator_class(
    #         queryset, per_page, orphans=orphans,
    #         allow_empty_first_page=allow_empty_first_page, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     content = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', content)


class UsersCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    # fields = '__all__'
    form_class = AdminUserEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context




#
# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     content = {'title': title, 'update_form': user_form}
#
#     return render(request, 'adminapp/user_update.html', content)

class UsersUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    #fields = '__all__'
    form_class = AdminUserEditForm

    def get_queryset(self):

        return super().get_queryset().select_related('shopuserprofile')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактирование'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     content = {'title': title, 'update_form': edit_form}
#
#     return render(request, 'adminapp/user_update.html', content)

class UsersDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')
    # fields = '__all__'
    form_class = ShopUserEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'пользователи/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'пользователи/удаление'
#
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         # user.delete()
#         # вместо удаления лучше сделаем неактивным
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('admin:users'))
#
#     content = {'title': title, 'user_to_delete': user}
#
#     return render(request, 'adminapp/user_delete.html', content)


class CategoryListView(ListView):
    model=ProductCategory
    template_name = 'adminapp/categories.html'
    paginate_by = 4

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории'
        return context



#
# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     title = 'админка/категории'
#
#     categories_list = ProductCategory.objects.all()
#
#     content = {
#         'title': title,
#         'objects': categories_list
#     }

    # return render(request, 'adminapp/categories.html', content)



class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    # fields = '__all__'
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context

#
# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     title = 'категории/создание'
#
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         category_form = ProductCategoryEditForm()
#
#     content = {'title': title, 'update_form': category_form}
#
#     return render(request, 'adminapp/category_update.html', content)


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    # fields = '__all__'
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)

#
# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категории/редактирование'
#     edit_category =  get_object_or_404(ProductCategory, pk=pk)
#
#
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:category_update', args=[edit_category.pk]))
#     else:
#         category_form = ProductCategoryEditForm(instance=edit_category)
#
#     content = {'title': title, 'update_form': category_form}
#
#     return render(request, 'adminapp/category_update.html', content)

class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/удаление'
        return context

#
# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     title = 'категории/удаление'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#     product = Product.objects.filter(category=pk)
#
#
#     if request.method == 'POST':
#
#         for prod in product:
#             prod.is_active = False
#             prod.save()
#
#         category.is_active = False
#         category.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#
#     content = {'title': title, 'category_to_delete': category}
#
#     return render(request, 'adminapp/category_delete.html', content)


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 6

    def get_queryset(self):
        category = self.kwargs.get('pk', '')
        q = super().get_queryset()
        return q.filter(category__pk=category).order_by('-is_active').select_related('category')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('pk', '')
        context['title'] = 'админка/продукты'
        name_category = ProductCategory.objects.filter(pk=category).first()
        context['category'] = category
        context['name_category'] = name_category
        return context



#
# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     title = 'админка/продукт'
#
#     category = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category__pk=pk).order_by('name')
#
#     content = {
#         'title': title,
#         'category': category,
#         'objects': products_list,
#     }
#
#     return render(request, 'adminapp/products.html', content)


# class ProductCreateView(CreateView):
#
#     model = Product
#     template_name = 'adminapp/product_create.html'
#     form_class = ProductEditForm
#     success_url = reverse_lazy('admin:categories')
#
#
#     @method_decorator(user_passes_test(lambda u: u.is_superuser))
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'товар/создание'
#         category = ProductCategory.objects.all()
#         context['category'] = category
#         return context

@user_passes_test(lambda u: u.is_superuser)

def product_create(request, pk):
    title = 'товар/создание'
    category_list = ProductCategory.objects.all()


    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)

        print(Gallery.name_gallery)
        product_gallery = GalleryEditForm(request.POST, request.FILES)

        if product_form.is_valid() and product_gallery.is_valid():

            t = product_form.save()

            if 'hot_image' in  request.FILES:
                t.gallery.hot_image = request.FILES['hot_image']
                t.gallery.save()

            if 'image_product' in request.FILES:
                t.gallery.image_product = request.FILES['image_product']
                t.gallery.save()

            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        product_form = ProductEditForm()
        product_gallery = GalleryEditForm()


    content = {'title': title, 'product_form': product_form, 'category': category_list, 'product_gallery': product_gallery}
    return render(request, 'adminapp/product_create.html', content)

        # instance = request.name_gallery.gallery
        # print(product_form['category'].value(), "value")
        # print(pk, 'pk')
        # gallery_form = GalleryEditForm(request.POST, request.FILES)

    #     if product_form.is_valid():
    #         post_name = request.POST['name']
    #         # prod = Product.objects.filter(name=post_name).first()
    #
    #         product_form.save()
    #         # gallery_form.save()
    #         #return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    #         # product_form = ProductEditForm(request.POST, request.FILES)
    #
    #     # if gallery_form.is_valid():
    #     #     gallery_form.save()
    #     #     print(pk)
    #
    #         return HttpResponseRedirect(reverse('admin:products', args=[int(pk)]))
    # else:
    #     product_form = ProductEditForm()
    #     gallery_form = GalleryEditForm()


    # content_pk = pk
    # # gallery_new = Gallery.objects.filter(name_gallery__pk=prod.pk)
    # # print(gallery_new)
    # print(pk)



class ProductListView(DetailView):
    model = Product
    template_name = 'adminapp/product.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/продукт описание'
        return context



#
# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     title = 'админка/продукт описание'
#
#     product = get_object_or_404(Product, pk=pk)
#
#
#     content = {
#         'title': title,
#         'product': product,
#     }
#
#     return render(request, 'adminapp/product.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'
    edit_product = get_object_or_404(Product, pk=pk)
    edit_gallery = get_object_or_404(Gallery, name_gallery=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        product_gallery = GalleryEditForm(request.POST, request.FILES, instance=edit_gallery)

        if product_form.is_valid() and product_gallery.is_valid():
            t = product_form.save()

            if 'hot_image' in request.FILES:
                t.gallery.hot_image = request.FILES['hot_image']
                t.gallery.save()

            if 'image_product' in request.FILES:
                t.gallery.image_product = request.FILES['image_product']
                t.gallery.save()
            return HttpResponseRedirect(reverse('admin:products', args=[int(edit_product.category.pk)]))
    else:
        product_form = ProductEditForm(instance=edit_product)
        product_gallery = GalleryEditForm(instance=edit_gallery)
    content = {'title': title, 'update_form': product_form, 'update_form_gallery': product_gallery}

    return render(request, 'adminapp/product_update.html', content)





@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт/удаление'

    product = get_object_or_404(Product, pk=pk)
    print(product.category.pk)

    if request.method == 'POST':
        # user.delete()
        # вместо удаления лучше сделаем неактивным
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin:products', args=[int(product.category.pk)]))

    content = {'title': title, 'product_to_delete': product}

    return render(request, 'adminapp/product_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def orders_list(request, pk=None):
    print(pk)
    if pk == 0:
        orders = Order.objects.order_by('-is_active')

    else:
        orders = Order.objects.filter(user=pk).order_by('-is_active')

    content ={
        'object_list': orders
    }
    return render(request, 'adminapp/orders.html', content)


@user_passes_test(lambda u: u.is_superuser)
def order_status(request, pk):
    print(pk)
    orders = Order.objects.filter(id=pk).first()
    print(orders.user.pk)
    st = Order.ORDER_STATUS_CHOICES
    t = 0
    while t < len(st):
        if st[t][0] == orders.status:
            if t+1 == len(st):
                t = -1
            orders.status = st[t+1][0]
            orders.save()
            break
        t = t + 1
    print(pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #return HttpResponseRedirect(reverse('admin:admin_orders', args=[orders.user.pk]))





@user_passes_test(lambda u: u.is_superuser)
def order_recover(request, pk):
    orders = Order.objects.filter(id=pk).first()
    orders.is_active = True
    orders.save()

    return HttpResponseRedirect(reverse('admin:admin_orders', args=[0]))


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]

'''
@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)

'''
