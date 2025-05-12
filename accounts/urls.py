# accounts/urls.py
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
from .forms import CustomLoginForm

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html', authentication_form=CustomLoginForm), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='update_profile'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('logout/', views.logout_view, name='logout'),
]
