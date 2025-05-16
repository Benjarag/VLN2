from django.urls import path
from . import views

app_name = 'offers'

urlpatterns = [
    path('<int:property_id>/offer/', views.submit_purchase_offer, name='submit_purchase_offer'),
    path('respond-offer/<int:offer_id>/', views.respond_to_offer, name='respond_to_offer'),
    path('', views.purchase_offers_list, name='offers'),
    path('myoffers/', views.seller_offers_list, name='myoffers'),
    path('offers/<int:offer_id>/finalize/contact/', views.contact_info_view, name='contact_info'),
    path('offers/<int:offer_id>/finalize/payment/', views.payment_method_view, name='payment_method'),
    path('finalization/<int:finalization_id>/review/', views.review_purchase, name='review_purchase'),
    path('confirmation/<int:finalization_id>/', views.purchase_confirmation, name='purchase_confirmation'),
    path('update/<int:offer_id>/', views.respond_to_offer, name='update_offer_status')
]