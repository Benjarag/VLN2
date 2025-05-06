# properties/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_listings, name='property_listings'),
    path('<int:property_id>/', views.property_details, name='property_details'),

]
