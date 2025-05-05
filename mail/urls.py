# mailapp/urls.py

from django.urls import path
from . import views

app_name = 'mailapp'

urlpatterns = [
    path('send-confirmation-email/<int:transaction_id>/', views.send_purchase_confirmation_email, name='send_confirmation_email'),
]
