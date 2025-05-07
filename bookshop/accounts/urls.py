from django.urls import path
from .views import register, login
from django.contrib.auth import views as auth_views
from main.views import user_logout

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', user_logout, name='logout')
]