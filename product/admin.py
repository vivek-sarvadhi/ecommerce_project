from django.contrib import admin
from product.models import ProductCategory, Product, Cart, CartProduct, Order, Rating
# Register your models here.

class ProductCategoryAdmin(admin.ModelAdmin):
	list_display = ('name','desc')


class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'desc', 'image', 'product_category_id', 'price')
	search_fields = ('name',)



admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(Rating)