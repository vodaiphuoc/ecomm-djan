from django.urls import path

from orders.views import checkout, order_complete, order_history

app_name = 'orders'

urlpatterns = [
    path('checkout', checkout, name='checkout'),
    path('order-complete/<int:order_id>', order_complete, name='order_complete'),
    path('order-history', order_history, name='order_history')
]
