from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('<int:property_id>/offer/', views.submit_purchase_offer, name='submit_purchase_offer'),
    path('respond-offer/<int:offer_id>/', views.respond_to_offer, name='respond_to_offer'),
    path('', views.purchase_offers_list, name='offers'),
    path('myoffers/', views.seller_offers_list, name='myoffers'),
    path('finalization/<int:finalization_id>/review/', views.review_purchase, name='review_purchase'),
    path('<int:offer_id>/finalize/', views.finalize_purchase, name='finalize_purchase'),
    # path('<int:offer_id>/cancel/', views.cancel_offer, name='cancel_offer'),
]