import django_filters
from product.models import CartProduct, Product, Rating
from django_filters.rest_framework import filters
from django.db.models import Avg
# from rest_framework import filters


class CartFilter(django_filters.FilterSet):
    product = django_filters.CharFilter(field_name='product__name', lookup_expr='icontains')
    category_name = django_filters.CharFilter(field_name='product__product_category_id__name', lookup_expr='exact')
    min_price = django_filters.NumberFilter(field_name='rate', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='rate', lookup_expr='lte')

    class Meta:
        model = CartProduct
        fields = ('product','min_price','max_price','category_name')





class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category_name = django_filters.CharFilter(field_name='product_category_id__name', lookup_expr='exact')
    # rating = django_filters.NumberFilter(field_name='product__ratings', lookup_expr='gte')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    # projectallocation_set = django_filters.CharFilter(field_name='ratinds_set__rating')   
    # rating = filters.RelatedFilter(RatingFilter, field_name='rating', queryset=Rating.objects.all())
   


    class Meta:
        model = Product
        fields = ('name','min_price','max_price','category_name','rating')

   
    rating = django_filters.NumberFilter(method='get_rating', field_name='ratings')


    def get_rating(self, queryset, rating, value):
        ratingavg = self.data['rating']
        rating_query = []
        for i in queryset:
            object = i.ratings.all().aggregate(Avg('rating'))
            obj1 = object['rating__avg']
            if obj1 == float(ratingavg):
                print("hello")
                product_obj = i.id
                rating_query.append(product_obj)
            else:
                print("hii")
        print(rating_query)
        queryset1 = Product.objects.filter(pk__in=rating_query)
        return queryset1



# class RatingFilter(django_filters.FilterSet):
#     # name = django_filters.CharFilter(lookup_expr='icontains')
#     # category_name = django_filters.CharFilter(field_name='product_category_id__name', lookup_expr='exact')
#     # min_price = django_filters.NumberFilter(field_name='product__price', lookup_expr='gte')
#     # max_price = django_filters.NumberFilter(field_name='product__price', lookup_expr='lte')
#     rating = django_filters.NumberFilter(field_name='rating', lookup_expr='exact')

#     class Meta:
#         model = Rating
#         fields = ('rating')
# class RatingFilter(django_filters.FilterSet):
#     rat