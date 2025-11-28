from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'e_commerce'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('health/', include('health_check.urls')),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('login/', views.CustomLoginView.as_view(),name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'),name='logout'),
    path('register/', views.register, name='register'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]
