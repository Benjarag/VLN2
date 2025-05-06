# mailapp/urls.py

from django.urls import path
from . import views

app_name = 'mail'

urlpatterns = [
    path('', views.mail_view, name='mail'),
]
