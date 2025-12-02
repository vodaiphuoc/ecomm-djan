from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('carts/', include('carts.urls')),
    path('orders/', include('orders.urls')),
    path('', include('products.urls')),
    path('health', include('health_check.urls')),
]
