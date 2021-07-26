from django import forms
from product.models import ProductCategory, Product, Order


class ProductCategoryForm(forms.ModelForm):
	class Meta:
		model = ProductCategory
		fields = ('name', 'desc')
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter product category name'}),
			'desc': forms.Textarea(attrs={'class':'form-control', 'placeholder':'enter product description'}),
		}


class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ('name','desc','image','product_category_id','price')
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter product name'}),
			'desc': forms.Textarea(attrs={'class':'form-control', 'placeholder':'enter product description'}),
			'image': forms.FileInput(attrs={'class':'form-control'}),
			'product_category_id': forms.Select(attrs={'class':'form-control', 'placeholder':'product category id'}),
			'price': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'enter product price'}),
		}


class CheckOutForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ('ordered_by', 'shipping_address', 'mobile', 'email')