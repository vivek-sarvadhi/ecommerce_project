from django.db.models import fields
from rest_framework import serializers
from product.models import ProductCategory, Product, Cart, CartProduct, Order, Rating
from django.db.models import Avg

class ProductCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    desc = serializers.CharField(required=True)
    
    class Meta:
        model = ProductCategory
        fields = ['name', 'desc']


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    desc = serializers.CharField(required=True)

    class Meta:
        model = Product
        fields = ['name', 'desc', 'image', 'product_category_id', 'price']


class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'desc', 'image', 'product_category', 'price','rating']

    product_category = serializers.SerializerMethodField('get_artist_name')
    rating = serializers.SerializerMethodField('get_average_rating')

    def get_artist_name(self, obj):
        return obj.product_category_id.name

    def get_average_rating(self, obj):
        return obj.ratings.all().aggregate(Avg('rating'))

        # counter = 0
        # avg_rat = 0
        # for rating_obj in obj.ratings.all():
        #     avg_rat += rating_obj.rating
        #     counter += 1
        # try:
        #     avg = avg_rat / counter
        #     return avg
        # except:
        #     return 0
        #     print("error")

    
# class RatingProductSerializer(serializers.ModelSerializer):
#     ratings = 
        

class CartProductSerializer(serializers.ModelSerializer):
    product = serializers.CharField(required=True)

    class Meta:
        model = CartProduct
        fields = ['product']


class CartListProductSerializer(serializers.ModelSerializer):
    product = serializers.CharField(required=True)
    # product_name = serializers.RelatedField(read_only=True)

    class Meta:
        model = CartProduct
        fields = ['product','rate','quantity','subtotal']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['mobile','shipping_address','discount']


class RatingSerializer(serializers.ModelSerializer):
    review = serializers.CharField(required=False)

    class Meta:
        model = Rating
        fields = ['product','rating', 'review']

