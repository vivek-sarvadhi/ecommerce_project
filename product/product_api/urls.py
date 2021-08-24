from django.urls import path
from product.product_api.views import (IndexAPIView, ProductCategoryAPIView, 
                                        ProductAPIView, CartProductAPIView, CartProductListAPIView, 
                                        OrderAPIView, CartProductRemoveAPIView, CartProductRemoveQuentityAPIView, 
                                        ProductListAPIView, ProductUpdateAPIView, ProductDestroyAPIView, RatingAPIView, RatingUpdateAPIView)


urlpatterns = [
    path('apiindex/', IndexAPIView.as_view(), name="index_api"),

    # product
    path('productcategory/', ProductCategoryAPIView.as_view(), name="product_category"),
    path('product/', ProductAPIView.as_view(), name="product"),
    path('productlist/', ProductListAPIView.as_view(), name="productlist"),
    path('productupdate/<int:pk>', ProductUpdateAPIView.as_view(), name="productupdate"),
    path('productdelete/<int:pk>', ProductDestroyAPIView.as_view(), name="productdelete"),

    # cart
    path('cartproduct/', CartProductAPIView.as_view(), name="cart_product"),
    path('cartproductremove/', CartProductRemoveAPIView.as_view(), name="cart_product_remove"),
    path('cartproductquentityremove/', CartProductRemoveQuentityAPIView.as_view(), name="cart_product__quentity_remove"),
    path('cartproductlist/', CartProductListAPIView.as_view(), name="cart_product_list"),

    # order
    path('order/', OrderAPIView.as_view(), name="order"),

    # rating
    path('rating/', RatingAPIView.as_view(), name='rating'),
    path('ratingupdate/<int:pk>', RatingUpdateAPIView.as_view(), name="ratingupdate"),
]