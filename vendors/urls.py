from django.urls import path
from . import views


urlpatterns = [
    path('vendors/', views.vendor_list),
    path('vendors/<int:vendor_id>/', views.vendor_detail),
    path('purchase_orders/', views.purchase_order_list),
    path('purchase_orders/<int:po_id>/', views.purchase_order_detail),
    path('purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order, name='acknowledge_purchase_order'),
    path('vendors/<int:vendor_id>/performance/', views.vendor_performance, name='vendor_performance'),
    
]

