from django.shortcuts import render, get_object_or_404, redirect
from product.models import ProductCategory, Product, Cart, CartProduct, Order
from product.forms import ProductCategoryForm, ProductForm, CheckOutForm
from django.views.generic import View, CreateView, ListView, DeleteView, UpdateView, DetailView, TemplateView
from django.urls import reverse, reverse_lazy

# Create your views here.
class ProductCategoryDetailView(ListView):
    model = ProductCategory
    template_name = "product/product_category_detail.html"
    context_object_name = "productcategory"


class ProductCategoryAddView(CreateView):
    template_name = "product/product_category_add.html"
    form_class = ProductCategoryForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product_category')


class ProductCategoryUpdateView(UpdateView):
    template_name = "product/product_category_add.html"
    form_class = ProductCategoryForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(ProductCategory, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("product_category")


class ProductCategoryDeleteView(DeleteView):
    template_name = "product/product_category_delete.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(ProductCategory, id=id_)

    def get_success_url(self):
        return reverse('product_category')


class ProductListForm(ListView):
    model = Product
    template_name = "product/product_list.html"
    context_object_name = "product"
    paginate_by = 3
    queryset = Product.objects.all()

    def get_queryset(self):
        name = self.request.GET.get('q')
        object_list = self.model.objects.all()
        if name:
            object_list = object_list.filter(name__icontains=name)
        return object_list


class ProductDetailForm(DetailView):
    template_name = "product/product_detail.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Product, id=id_)


class ProductAddForm(CreateView):
    template_name = 'product/product_add.html'
    form_class = ProductForm

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product')


class ProductUpdateForm(UpdateView):
    template_name = 'product/product_add.html'
    form_class = ProductForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Product, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product')


class ProductDeleteForm(DeleteView):
    template_name = 'product/product_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Product, id=id_)

    def get_success_url(self):
        return reverse('product')


class AddToCartView(TemplateView):
    template_name = "product/addtocart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['id']
        product_obj = Product.objects.get(id=product_id)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(product=product_obj)
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, 
                                rate=product_obj.price, quantity=1, subtotal=product_obj.price)
                cart_obj.total += product_obj.price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, 
                                rate=product_obj.price, quantity=1, subtotal=product_obj.price)
            cart_obj.total += product_obj.price
            cart_obj.save()
        return context


class ManageCartView(View):

    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == "rmv":
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("mycart")


class EmptyCartView(View):

    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect("mycart")


class MyCartView(TemplateView):
    template_name = "product/mycart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


class CheckOutView(CreateView):
    template_name = "product/checkout.html" 
    form_class = CheckOutForm
    success_url = reverse_lazy("product")


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 2:
            pass
        else:
            return redirect("/users/login/?next=/product/checkout/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context["cart"] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get("cart_id")
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.oreder_status = "Order Received"
            del self.request.session['cart_id']
        else:
            return redirect("product")
        return super().form_valid(form)






# class ProductDetailForm(ListView):
#   model = Product
#   template_name = "product/product_detail.html"
#   context_object_name = "product"


# class ProductAddForm(CreateView):
#   template_name = "product/product_add.html"
#   form_class = ProductForm

#   def form_valid(self, form):
#       return super().form_valid(form)

#   def get_success_url(self):
#       return reverse(product)