from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import HttpRequest

from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Product, Order, OrderItem
from .cart import Cart

TEMPLATE_FOLDER_NAME = 'e_commerce'

def product_list(request: HttpRequest):
    query = request.GET.get('q')
    products = Product.objects.all().order_by('-created_at')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, f'{TEMPLATE_FOLDER_NAME}/product_list.html', {'page_obj': page_obj, 'query': query})

def product_detail(request: HttpRequest, id):
    product = get_object_or_404(
        Product.objects.prefetch_related('reviews__user'),
        id=id
    )
    return render(request, f'{TEMPLATE_FOLDER_NAME}/product_detail.html', {'product': product})

@require_POST
def cart_add(request: HttpRequest, product_id: int):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    messages.success(request, "Added to cart")
    return redirect(f'{TEMPLATE_FOLDER_NAME}:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect(f'{TEMPLATE_FOLDER_NAME}:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, f'cart.html', {'cart': cart})

def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        # Create Order
        order = Order.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            postal_code=request.POST.get('postal_code'),
            city=request.POST.get('city'),
            total_cost=cart.get_total_price()
        )
        
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
            
        cart.clear()
        messages.success(request, "Order created successfully!")
        return render(request, f'order_created.html', {'order': order})
        
    return redirect(f'{TEMPLATE_FOLDER_NAME}:cart_detail')
