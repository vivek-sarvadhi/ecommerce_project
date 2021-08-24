from django.db import models
from django.conf import settings
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class ProductCategory(models.Model):
	name = models.CharField(max_length=100)
	desc = models.TextField()
	# slug = models.SlugField(max_length=100, unique=True)
	is_delete = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=100)
	desc = models.TextField()
	# slug = models.SlugField(max_length=100, unique=True)
	image = models.ImageField(upload_to='product_image/', blank=True, null=True)
	product_category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, blank=True)
	price = models.IntegerField()
	is_delete = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


	def __str__(self):
		return self.name


class Cart(models.Model):
    customer = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart: " + str(self.id)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)


class Order(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	ordered_by = models.CharField(max_length=200)
	shipping_address = models.CharField(max_length=200)
	mobile = models.CharField(max_length=10)
	email = models.EmailField(null=True, blank=True)
	subtotal = models.PositiveIntegerField()
	discount = models.PositiveIntegerField()
	total = models.PositiveIntegerField()
	oreder_status = models.CharField(max_length=50, choices=ORDER_STATUS)
	is_delete = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


	def __str__(self):
		return "order: " + str(self.id)


class Rating(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	review = models.CharField(max_length=100, null=True, blank=True)

