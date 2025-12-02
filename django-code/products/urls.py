from django.urls import path

from products.views import product_list, product_detail

app_name = 'products'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('category/<slug:category_slug>/<int:category_id>', product_list, name='category_product_list'),
    path('detail/<int:id>', product_detail, name='product_detail'),
]
