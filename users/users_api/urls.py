from django.urls import path
from users.users_api.views import IndexAPIView, LoginRegisterAPIView


urlpatterns = [
    path('login_register/', LoginRegisterAPIView.as_view(), name="login_register_api"),
]