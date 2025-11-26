from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Product, Order, OrderItem
from .cart import Cart
from .forms import AppUserCreationForm, OrderForm
from django.views.decorators.cache import cache_control
from django.db import transaction

TEMPLATE_FOLDER_NAME = 'e_commerce'

def register(request):
    if request.method == 'POST':
        form = AppUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect(f'/')
    else:
        form = AppUserCreationForm()
    
    return render(request, f'{TEMPLATE_FOLDER_NAME}/register.html', {'form': form})

class CustomLoginView(UserPassesTestMixin, LoginView):
    template_name = f'{TEMPLATE_FOLDER_NAME}/login.html'

    def test_func(self)->bool:
        r"""return True if the user is NOT authenticated"""
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        next_url = self.request.GET.get('next')
        print('next url: ', next_url)
        if next_url:
            return redirect(next_url)
        
        return redirect(f'/')

def product_list(request: HttpRequest):
    query = request.GET.get('q')
    products = Product.objects.all().order_by('-created_at')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, f'{TEMPLATE_FOLDER_NAME}/product_list.html', {'page_obj': page_obj, 'query': query})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_detail(request: HttpRequest, id):
    product = get_object_or_404(
        Product.objects.prefetch_related('reviews__user'),
        id=id
    )
    return render(request, f'{TEMPLATE_FOLDER_NAME}/product_detail.html', {'product': product})

@require_POST
@login_required(login_url='/login/')
def cart_add(request: HttpRequest, product_id: int):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    messages.success(request, "Added to cart")
    return redirect(f'{TEMPLATE_FOLDER_NAME}:cart_detail')

def cart_remove(request: HttpRequest, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect(f'{TEMPLATE_FOLDER_NAME}:cart_detail')

def cart_detail(request: HttpRequest):
    cart = Cart(request)
    return render(request, f'{TEMPLATE_FOLDER_NAME}/cart.html', {'cart': cart, 'form': OrderForm()})

@require_POST
def checkout(request: HttpRequest):
    cart = Cart(request)
    
    form = OrderForm(request.POST)

    if form.is_valid():
        try:
            with transaction.atomic():
                order: Order = form.save(commit=False)
                
                # Assign user if authenticated
                if request.user.is_authenticated:
                    order.user = request.user
                
                order.total_cost = cart.get_total_price()
                order.save()

                
                order_items_to_commit = []
                for item in cart:
                    product = item['product']
                    quantity = item['quantity']
                    
                    
                    # Stock check
                    if product.stock < quantity:
                        raise ValueError(f"Not enough stock for {product.name}.")
                    

                    order_items_to_commit.append(
                        OrderItem(
                            order=order,
                            product=product,
                            quantity=quantity
                    ))
                    
                    # Deduct stock immediately
                    product.stock -= quantity
                    product.save()
                
                OrderItem.objects.bulk_create(order_items_to_commit) 
                
                
                # Clear cart and success message
                cart.clear()
                messages.success(request, "Order created successfully! 🎉")
                
                return render(request, f'{TEMPLATE_FOLDER_NAME}/order_created.html', {'order': order})

        except ValueError as e:
            # Handle out-of-stock
            print(e)
            messages.error(request, f"Order failed: {e}")
            return redirect(f'{TEMPLATE_FOLDER_NAME}:cart_detail')

        except Exception as e:
            print(e)
            # Handle general database/server errors
            messages.error(request, "An unexpected error occurred during checkout.")
            return redirect(f'{TEMPLATE_FOLDER_NAME}:cart_detail')
    
    # the form is NOT valid
    else:
        messages.error(request, "Please correct the errors in the form.")
        return render(request, f'{TEMPLATE_FOLDER_NAME}/cart.html', {'form': form, 'cart': cart})