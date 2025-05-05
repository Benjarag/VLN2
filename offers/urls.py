from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('', views.offers, name='my_offers'),
]
