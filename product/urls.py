from django.urls import path, include
from product.views import (ProductCategoryDetailView, ProductListForm, 
							ProductCategoryAddView, ProductCategoryUpdateView, 
							ProductCategoryDeleteView, ProductDetailForm, 
							ProductAddForm, ProductUpdateForm, 
							ProductDeleteForm, AddToCartView,
							MyCartView, ManageCartView, EmptyCartView,
							CheckOutView, product_filter,

						)

urlpatterns = [

	path('api/', include('product.product_api.urls')),

	path('productcategory/', ProductCategoryDetailView.as_view(), name="product_category"),
	path('productcategoryadd/', ProductCategoryAddView.as_view(), name="product_category_add"),
	path('productcategoryupdate/<int:id>/', ProductCategoryUpdateView.as_view(), name="product_category_update"),
	path('productcategorydelete/<int:id>/', ProductCategoryDeleteView.as_view(), name="product_category_delete"),
	
	path('product/', ProductListForm.as_view(), name="product"),
	path('product/<int:id>', ProductDetailForm.as_view(), name="productdetail"),
	path('productadd/', ProductAddForm.as_view(), name="product_add"),
	path('productupdate/<int:id>/', ProductUpdateForm.as_view(), name="product_update"),
	path('productdelete/<int:id>/', ProductDeleteForm.as_view(), name="product_delete"),


	path('addtocart/<int:id>/', AddToCartView.as_view(), name="add_to_cart"),
	path('mycart/', MyCartView.as_view(), name="mycart"),
	path('managecart/<int:cp_id>/', ManageCartView.as_view(), name="manage_cart"),
	path('emptycart/', EmptyCartView.as_view(), name="empty_cart"),

	path('checkout/', CheckOutView.as_view(), name="check_out"),

	path('product_filter', product_filter, name='product_filter')
]