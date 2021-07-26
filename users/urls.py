from django.urls import path
from users.views import IndexView, RegisterView, LoginView, ProfileView, PasswordChangeView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
	path('index/', IndexView.as_view(), name="index"),
	path('register/', RegisterView.as_view(), name="register"),
	path('profile/<int:pk>', ProfileView.as_view(), name="profile"),
	path('login/', LoginView.as_view(), name="login"),
	path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),

	path('change-password/', PasswordChangeView.as_view(), name='change_password'),

	path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html',
		subject_template_name='users/password_reset_subject.txt',email_template_name='users/password_reset_email.html',),
		name="password_reset"),
	path('password-reset/done/',
		 auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
		 name='password_reset_done'),
	path('password-reset-confirm/<uidb64>/<token>/',
		 auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
		 name='password_reset_confirm'),
	path('password-reset-complete/',
		 auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
		 name='password_reset_complete'),
]
