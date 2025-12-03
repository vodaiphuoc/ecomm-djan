from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpRequest
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.db import transaction
from urllib.parse import urlencode

from orders.models import Order, OrderItem
from carts.cart import Cart
from orders.forms import OrderForm
from orders.utils import generate_qr_code

TEMPLATE_FOLDER_NAME = 'orders'

@require_POST
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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
                
                # make as success for demo purpose only
                order.payment_status = 'SUCCESS'
                order.save()

                return redirect(f'{TEMPLATE_FOLDER_NAME}:order_complete', order_id = order.id)

        except ValueError as e:
            # Handle out-of-stock
            print(e)
            messages.error(request, f"Order failed: {e}")
            return redirect(f'carts:cart_detail')

        except Exception as e:
            print(e)
            # Handle general database/server errors
            messages.error(request, "An unexpected error occurred during checkout.")
            return redirect(f'carts:cart_detail')
    
    # the form is NOT valid
    else:
        messages.error(request, "Please correct the errors in the form.")
        return render(request, f'carts/cart.html', {'form': form, 'cart': cart})


@login_required(login_url='/login/')
def order_complete(request: HttpRequest, order_id: int):
    r"""GET request to view specific order"""

    try:
        order = Order.objects.get(id=order_id, user = request.user)

    except Order.DoesNotExist:
        messages.error(request, "Page not found.")
        return redirect('/')

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


@login_required
def order_history(request: HttpRequest):
    """
    Fetches all orders associated with the currently logged-in user.
    Orders are retrieved in descending order of creation time.
    """
    try:
        # Query the database for orders belonging to the current user (request.user)
        # We use .select_related('user') to optimize the initial query
        # and .prefetch_related('items__product') to efficiently load all related OrderItems and their Products
        orders = Order.objects.filter(user=request.user).select_related('user').prefetch_related('items__product')

        return render(
            request, 
            f'{TEMPLATE_FOLDER_NAME}/order_history.html', 
            {
                'orders': orders,
                'user': request.user
            }
        )

    except Exception as e:
        print(f"Error fetching order history: {e}")
        return render(
            request, 
            f'{TEMPLATE_FOLDER_NAME}/order_history.html', 
            {
                'orders': [],
                'error_message': 'Could not retrieve order history due to an internal error.'
            }
        )