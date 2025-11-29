from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_control
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.db.models import Q

TEMPLATE_FOLDER_NAME = 'e_commerce'

from e_commerce.forms import ReviewForm
from e_commerce.models import Product, Order

def product_list(request: HttpRequest):
    query = request.GET.get('q')
    products = Product.objects.all().order_by('-created_at')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(
        request, 
        f'{TEMPLATE_FOLDER_NAME}/product_list.html', 
        {
            'page_obj': page_obj, 
            'query': query
        }
    )

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_detail(request: HttpRequest, id:int):
    try:
        product = get_object_or_404(
            Product.objects.prefetch_related('reviews__user'),
            id=id
        )

        rounded_mean_rating = round(product.mean_rating*100,1) if product.mean_rating else None
        
        allow_to_review = None
        if request.user.is_authenticated:
            allow_to_review: bool = Order.objects.filter(
                user = request.user,
                items__product=product
            ).exists()
        else:
            allow_to_review = False

        return render(
            request, 
            f'{TEMPLATE_FOLDER_NAME}/product_detail.html', 
            {
                'product': product,
                'mean_rating': rounded_mean_rating,
                'allow_to_review': allow_to_review,
                'review_form': ReviewForm()
            }
        )
    except Exception as e:
        print(e)
        raise e
