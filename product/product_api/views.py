from typing_extensions import ParamSpecKwargs
from rest_framework.generics import ListAPIView, CreateAPIView, GenericAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from product.product_api.serializers import (ProductCategorySerializer, ProductSerializer, 
                                                CartProductSerializer, OrderSerializer, 
                                                CartListProductSerializer, ProductListSerializer,
                                                RatingSerializer,
                                            )
from rest_framework import viewsets, filters
from product.models import Cart, CartProduct, Product, Rating
# from product.product_api.pagination import PaginationHandlerMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from product.product_api.pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from product.product_api.filters import CartFilter, ProductFilter
from product.product_api.permissions import IsSeller, IsCustomer


class IndexAPIView(ListAPIView):

    def get(self, request, *args, **kwargs):
        return Response(data={'status':status.HTTP_202_ACCEPTED,'Message':'Hello world'},status=status.HTTP_202_ACCEPTED)


class ProductCategoryAPIView(CreateAPIView):
    permission_classes = [IsSeller]

    def post(self, request, *args, **kwargs):
        serializer = ProductCategorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,'Message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid:
            name = serializer.validated_data['name']
            desc = serializer.validated_data['desc']
            serializer.save()
            return Response(data={'status':status.HTTP_201_CREATED,'Message':"Created successfully",'Result':{'name':name, 'desc':desc }},status=status.HTTP_201_CREATED)


class ProductAPIView(CreateAPIView):
    permission_classes = [IsSeller]

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,'Message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(data={'status':status.HTTP_201_CREATED,'Message':"Created successfully"},status=status.HTTP_201_CREATED)


class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = ProductFilter

    def get_queryset(self):
        
        queryset = Product.objects.all()
        return queryset


class ProductUpdateAPIView(UpdateAPIView):
    permission_classes = [IsSeller]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data={'status': status.HTTP_200_OK,"message": "product updatated successfully",'Result':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,"Message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProductDestroyAPIView(DestroyAPIView):
    permission_classes = [IsSeller]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    # def perform_destroy(self, instance):
    #     print(instance)
    #     instance.delete_flag = True
    #     instance.save()
    

    
class CartProductAPIView(GenericAPIView):
    queryset = CartProduct.objects.all()
    serializer_class = CartProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,'Message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            try:
                user = request.user
                cart = Cart.objects.filter(customer=user)
                product_id = request.data['product']
                quentity = 1
                product_obj = Product.objects.get(id=product_id)
                if cart:
                    cart = Cart.objects.filter(customer=user).last()
                    cart = Cart.objects.get(id=cart.id)
                    cartproduct = CartProduct.objects.filter(cart=cart, product=product_obj)
                    if cartproduct.exists():
                        cartproductid = cartproduct.last()
                        cartproductid.quantity += 1
                        cartproductid.subtotal = product_obj.price * cartproductid.quantity
                        cartproductid.save()
                        cart.total += product_obj.price
                        cart.save()
                        return Response(data={'status':status.HTTP_201_CREATED,'Message':"increase product quentity in cart", 'Result':{'product':product_obj.name,
                                                    'price':product_obj.price,'Quentity':cartproductid.quantity,'subtotal':cartproductid.subtotal,}},
                                                    status=status.HTTP_201_CREATED)
                    else:
                        if product_obj:
                            price = product_obj.price
                            subtotal = int(quentity) * price
                        serializer.validated_data['cart'] = cart
                        serializer.validated_data['product'] = product_obj
                        serializer.validated_data['rate'] = product_obj.price
                        serializer.validated_data['quantity'] = quentity
                        serializer.validated_data['subtotal'] = subtotal
                        cart.total += subtotal
                        cart.save()
                        serializer.save()
                else:
                    cart = Cart(customer=user)
                    if product_obj:
                            price = product_obj.price
                            subtotal = int(quentity) * price
                    serializer.validated_data['cart'] = cart
                    serializer.validated_data['product'] = product_obj
                    serializer.validated_data['rate'] = product_obj.price
                    serializer.validated_data['quantity'] = quentity
                    serializer.validated_data['subtotal'] = subtotal
                    cart.total += subtotal
                    cart.save()
                    serializer.save()
                    
                return Response(data={'status':status.HTTP_201_CREATED,'Message':"create product in cart", 'Result':{'product':product_obj.name,
                                                    'price':product_obj.price,'Quentity':quentity,'subtotal':subtotal, }},
                                                    status=status.HTTP_201_CREATED)
            except Product.DoesNotExist:
                return Response(data={'status':status.HTTP_404_NOT_FOUND,'Message':"Product id not fount"},status=status.HTTP_404_NOT_FOUND)


class CartProductListAPIView(ListAPIView):
    serializer_class = CartListProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['rate','product__name']
    filterset_class = CartFilter
    print("h=====>",filterset_class)


    def get_queryset(self):
        user = self.request.user
        # product_name = self.request.query_params.get('product__name', None)
        cart = Cart.objects.filter(customer=user)
        if cart:
            print(cart)
            for i in cart:
                queryset = CartProduct.objects.filter(cart=i)
                # for i in queryset:
                    # print(i.product.product_category_id)
                # if product_name is not None:
                #     queryset = CartProduct.objects.filter(product__name__icontains=product_name)
                # if queryset1:
                #     print('hello')
                #     return queryset1
                
                return queryset

class CartProductRemoveAPIView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        if request.data:
            product = request.data['product']
            user = request.user
            cart_obj = Cart.objects.filter(customer=user)
            print(cart_obj)
            cartproduct_obj = CartProduct.objects.filter(cart__in=cart_obj)
            for i in cartproduct_obj:
                cart_obj = Cart.objects.filter(customer=user).last()
                cart = Cart.objects.get(id=cart_obj.id)
                print(i.product.name)
                if i.product.id == int(product):
                    i.delete()
                    cart.total -= i.subtotal
                    print(cart.total)
                    cart.save()
                    return Response(data={'status':status.HTTP_205_RESET_CONTENT,'Message':"deleted product"}, status=status.HTTP_205_RESET_CONTENT)
            return Response(data={'status':status.HTTP_404_NOT_FOUND,'Message':"Not found product id"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,'Message':"please enter product id"}, status=status.HTTP_400_BAD_REQUEST)
        

class CartProductRemoveQuentityAPIView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        if request.data or request.query_params:
            delete_product = request.query_params.get('delete_product')
            user = request.user
            cart_obj = Cart.objects.filter(customer=user)
            cartproduct_obj = CartProduct.objects.filter(cart__in=cart_obj)
            for i in cartproduct_obj:
                cart_obj = Cart.objects.filter(customer=user).last()
                cart = Cart.objects.get(id=cart_obj.id)
                if delete_product:
                    if i.product_id == int(delete_product):
                        i.delete()
                        cart.total -= i.subtotal
                        print(cart.total)
                        cart.save()
                        return Response(data={'status':status.HTTP_205_RESET_CONTENT,'Message':"deleted product",}, status=status.HTTP_205_RESET_CONTENT)
                else:
                    product = request.data['product']
                    if i.product_id == int(product):
                        print(type(i.quantity))
                        if i.quantity > 1:
                            print("heloooooo")
                            i.quantity -= 1
                            i.subtotal -= i.rate
                            cart.total -= i.rate
                            cart.save()
                            i.save()
                            return Response(data={'status':status.HTTP_205_RESET_CONTENT,'Message':"remove one quentity",
                                                    'Result':{'product':i.product.name,'rate':i.rate,'quentity':i.quantity,'Subtotal':i.subtotal}}, 
                                                    status=status.HTTP_205_RESET_CONTENT)
                        else:
                            i.delete()
                            cart.total -= i.subtotal
                            print(cart.total)
                            cart.save()
                            return Response(data={'status':status.HTTP_205_RESET_CONTENT,'Message':"quentity zero deleted product",}, status=status.HTTP_205_RESET_CONTENT)
            return Response(data={'status':status.HTTP_205_RESET_CONTENT,'Message':"please enter valid id",}, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,'Message':"please enter product id"}, status=status.HTTP_400_BAD_REQUEST)



class OrderAPIView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,'Message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            mobile = request.data['mobile']
            shipping_address = request.data['shipping_address']
            discount = request.data['discount']
            user = request.user
            cart = Cart.objects.filter(customer=user).last()
            cart_obj = Cart.objects.get(id=cart.id)
            cartproduct_obj = CartProduct.objects.filter(cart=cart_obj)
            total = cart_obj.total - int(discount)
            if cartproduct_obj:
                serializer.validated_data['cart'] = cart_obj
                serializer.validated_data['ordered_by'] = user
                serializer.validated_data['email'] = user
                serializer.validated_data['mobile'] = mobile
                serializer.validated_data['shipping_address'] = shipping_address
                serializer.validated_data['subtotal'] = cart_obj.total
                serializer.validated_data['total'] = total
                serializer.validated_data['discount'] = discount
                serializer.save()
                cart.total = 0
                cart.save()
                cartproduct_obj = CartProduct.objects.filter(cart=cart_obj)
                cartproduct_obj.delete()
                return Response(data={'status':status.HTTP_200_OK,'Message':"Place order successfully",'Result':
                                        {'mobile':mobile,'shipping_address':shipping_address,'total':cart_obj.total,'discount':discount,'pay amount':total}},status=status.HTTP_200_OK)
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,'Message':"product not found in cart"},status=status.HTTP_400_BAD_REQUEST)


class RatingAPIView(CreateAPIView):
    permission_classes = [IsCustomer]

    def post(self, request, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,'Message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            product = request.data['product']
            product_obj = Product.objects.get(id=product)
            rating = request.data['rating']
            user = request.user
            p1 = serializer.validated_data['product'] = product_obj
            u1 = serializer.validated_data['rating'] = rating
            serializer.validated_data['user'] = user
            rating_obj = Rating.objects.all()
            for i in rating_obj:
                if i.product == p1 and i.user == user:
                    print("hiiii")
                    return Response(data={'status':status.HTTP_400_BAD_REQUEST,'Message':"already rating provide on product"},status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(data={'status':status.HTTP_200_OK,'Message':"rating on product",'Result':serializer.data},status=status.HTTP_200_OK)


class RatingUpdateAPIView(UpdateAPIView):
    permission_classes = [IsCustomer]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        user = request.user
        print(serializer)
        print(instance.user)

        if serializer.is_valid():
            if instance.user == user:
                serializer.save()
                return Response(data={'status': status.HTTP_200_OK,"message": "rating updatated successfully",'Result':serializer.data}, status=status.HTTP_200_OK)
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,"Message":'user does not match'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'status':status.HTTP_400_BAD_REQUEST,"Message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

