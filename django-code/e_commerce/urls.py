from django.urls import path, include
from django.contrib.auth import views as auth_views

from e_commerce.views import product, user, cart, review, order

app_name = 'e_commerce'

urlpatterns = [
    path('', product.product_list, name='product_list'),
    path('category/<slug:category_slug>/<int:category_id>', product.product_list, name='category_product_list'),
    path('health', include('health_check.urls')),
    path('product/<int:id>', product.product_detail, name='product_detail'),
    path('login', user.CustomLoginView.as_view(),name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='/'),name='logout'),
    path('register', user.register, name='register'),
    path('pwd_change', user.CustomPwdChangeView.as_view(),name='pwd_change'),
    path('cart/', cart.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>', cart.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>', cart.cart_remove, name='cart_remove'),
    path('checkout', order.checkout, name='checkout'),
    path('order-complete/<int:order_id>', order.order_complete, name='order_complete'),
    path('submit_review/<int:product_id>', review.submit_review, name='submit_review'),
]
