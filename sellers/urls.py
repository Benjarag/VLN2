from django.urls import path
from . import views


app_name = 'sellers'

urlpatterns = [
    path('<int:seller_id>/', views.seller_profile, name='seller_profile'),
    path('my-listings/', views.my_listings, name='my_listings'),
]