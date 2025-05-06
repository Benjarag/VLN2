# properties/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_listings, name='property_listings'),
    path('<int:property_id>/', views.property_detail, name='property_details'),

]
