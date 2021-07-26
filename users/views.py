from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.views import View
from users.models import CustomUser
from users.forms import CustomUserForm, ProfileUserForm, PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse
from Ecommerceproject import settings
from django.core.mail import send_mail 
from django.http import HttpResponse
from django.contrib.auth.views import PasswordContextMixin
from django.views.generic.edit import FormView
from django.utils.translation import gettext as _
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Create your views here.

# def index(request):
# 	return render(request, 'users/index.html')
class IndexView(View):

	def get(self, request):
		return render(request, 'users/index.html')

class RegisterView(View):
	
	def get(self, request):
		form = CustomUserForm()
		return render(request, 'users/registration_form.html', {'form':form})

	def post(self, request):
		if request.method == "POST":
			form = CustomUserForm(request.POST or request.FILES)
			if form.is_valid():
				email = form.cleaned_data.get('email')
				first_name = form.cleaned_data.get('first_name')
				last_name = form.cleaned_data.get('last_name')
				user_type = form.cleaned_data.get('user_type')
				password = form.cleaned_data.get('password')
				conf_password = request.POST.get('confirm_password')
				if password == conf_password:
					saved_user = form.save(commit=False)
					saved_user.set_password(password)
					subject = "Welcome to Ecommerce"
					message = f"hi {email}, your account is successfully created"
					to = "tiwarivivek389@gmail.com"
					res = send_mail(subject, message, settings.EMAIL_HOST_USER, [to])
					saved_user.save()
					return redirect('login')
				else:
					messages.error(request, "password or confirm password are not match")
					return render(request, 'users/registration_form.html', {'form':form})
				return render(request, 'users/registration_form.html', {'form':form})
			messages.error(request, "email id already used")
			return render(request, 'users/registration_form.html', {'form':form})


class LoginView(View):

	def get(self, request):
		form = CustomUserForm()
		return render(request, 'users/login_form.html', {'form':form})

	def post(self, request):
		form = CustomUserForm()
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(email=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('index')
		else:
			messages.error(request, "email or password is not correct")
			return render(request, 'users/login_form.html', {'form':form})
		return render(request, 'users/login_form.html', {'from':form})


class ProfileView(View):

	def get(self, request, pk):
		form = CustomUserForm()
		user1 = CustomUser.objects.get(pk=pk)
		return render(request, 'users/profile_form.html', {'form':form,'user1':user1})

	def post(self, request, pk):
		form = ProfileUserForm(request.POST or None, request.FILES or None, instance=request.user)
		if form.is_valid():
			form.save()
		else:
			print(form.errors)
		form = CustomUserForm()
		return render(request, 'users/profile_form.html', {'form':form})


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')
    template_name = 'users/change_password.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


