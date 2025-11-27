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
from django.views.decorators.cache import cache_control
from django.db import transaction
from urllib.parse import urlencode

from .models import Product, Order, OrderItem, Review
from .cart import Cart
from .forms import AppUserCreationForm, OrderForm, ReviewForm
from .utils import generate_qr_code

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
def product_detail(request: HttpRequest, id:int):
    product = get_object_or_404(
        Product.objects.prefetch_related('reviews__user'),
        id=id
    )
    
    allow_to_review: bool = Order.objects.filter(
        user = request.user,
        items__product=product
    ).exists()

    return render(
        request, 
        f'{TEMPLATE_FOLDER_NAME}/product_detail.html', 
        {
            'product': product,
            'allow_to_review': allow_to_review,
            'review_form': ReviewForm()
        }
    )

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
                
                # make as success for demo purpose only
                order.payment_status = 'SUCCESS'
                order.save()

                # fake bank account here
                payment_info = {
                    'acc': '000001111',
                    'bank': 'myAppBank',
                    'amount': order.total_cost,
                    'orderId': order.id
                }
                
                payment_url = request.build_absolute_uri(f"/mobile/img?{urlencode(payment_info)}")
                qr_data_uri = generate_qr_code(payment_url)

                return render(
                    request, 
                    f'{TEMPLATE_FOLDER_NAME}/order_created.html', 
                    {
                        'order': order,
                        'qr_data_uri': qr_data_uri
                    }
                )
            

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
    
@require_POST
def submit_review(request: HttpRequest, product_id: int):
    form = ReviewForm(request.POST)
    
    if form.is_valid():
        try:
            with transaction.atomic():
                
                review: Review = form.save(commit=False)

                product = Product.objects.get(id = product_id)
                review.product = product
                review.user = request.user

                review.save()
                return redirect(f'{TEMPLATE_FOLDER_NAME}:product_detail', id=product_id)

        except Product.DoesNotExist:
            messages.error(request, "The specified product does not exist.")
            return redirect(f'{TEMPLATE_FOLDER_NAME}:product_list')

        except Exception as e:
            messages.error(request, "An unexpected error occurred during process review.")
            return redirect(f'{TEMPLATE_FOLDER_NAME}:product_detail', id=product_id)

    else:
        messages.error(request, "Please correct the errors in the form.")
        return redirect(f'{TEMPLATE_FOLDER_NAME}:product_detail', id=product_id)