from django.http import HttpRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.cache import cache_control

TEMPLATE_FOLDER_NAME = 'carts'

from orders.forms import OrderForm
from carts.cart import Cart
from products.models import Product

@require_POST
@login_required(login_url='/login/')
def cart_add(request: HttpRequest, product_id: int):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    messages.success(request, "Added to cart")
    return redirect(request.GET.get('next'))

def cart_remove(request: HttpRequest, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect(f'{TEMPLATE_FOLDER_NAME}:cart_detail')

@login_required(login_url='/login/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart_detail(request: HttpRequest):
    cart = Cart(request)
    return render(request, f'{TEMPLATE_FOLDER_NAME}/cart.html', {'cart': cart, 'form': OrderForm()})
