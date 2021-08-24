from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class CustomUserManager(BaseUserManager):

	def create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError(_("The Email must be set"))
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user


	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)


		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('superuser must have is_staff=True.'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(_('superuser must have is_superuser=True'))
		return self.create_user(email, password, **extra_fields)


user_type_choice = (
		(1,'Seller'),
		(2,'Customer')
	)


class CustomUser(AbstractUser):
	username = None
	email = models.EmailField(_("email address"), unique=True)
	user_type = models.IntegerField(choices=user_type_choice, default=2)
	profile_image = models.ImageField(upload_to="profile/", default="../static/image/1.jpeg", blank=True, null=True)
	phone_number = models.CharField(max_length=10, blank=True, null=True)
	address = models.TextField(null=True, blank=True)
	is_delete = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)



	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	def __str__(self):
		return self.email


class CustomUserToken(models.Model):
    user = models.ForeignKey(CustomUser, related_name="customuser", on_delete=models.CASCADE)
    token = models.CharField(null=True, max_length=500)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return str(self.user)





