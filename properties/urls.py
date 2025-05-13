# properties/urls.py
from django.urls import path
from . import views

app_name = 'properties'  # Add namespace

urlpatterns = [
    path('', views.property_listings, name='property_listings'),
    path('<int:property_id>/', views.property_details, name='property_details'),
    path('<int:property_id>/offer/', views.submit_purchase_offer, name='submit_purchase_offer'),
]