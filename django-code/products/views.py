from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_control
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.contrib import messages
from django_ratelimit.decorators import ratelimit

TEMPLATE_FOLDER_NAME = 'products'

from reviews.forms import ReviewForm
from products.models import Product, Category
from orders.models import Order

@ratelimit(key='ip', rate='5/m', block=True)
def product_list(
        request: HttpRequest, 
        category_slug:str = None, 
        category_id: int = None
    ):
    
    parent_categories = Category.objects.filter(parent__isnull=True).order_by('name')
    categories_tree = parent_categories.prefetch_related(
        Prefetch('children', queryset=Category.objects.order_by('name'), to_attr='subcategories')
    )
    query = None

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')

    if price_min is not None and price_max is not None:
        try:
            price_min = int(price_min)
            price_max = int(price_max)
            assert price_max > price_min
            print(price_min, price_max)
        except Exception as e:
            messages.error(request, "giá trị min max không hợp lệ")
            redirect(request.path)

    if category_slug is not None and category_id is not None:
        target_parent_cate = categories_tree.filter(id=category_id).first()

        if target_parent_cate:
            sub_categories = target_parent_cate.subcategories
            products = []
            if price_min is not None and price_max is not None:
                for sub_cate in sub_categories:
                    products_queryset = sub_cate.products.filter(price__gte=price_min).filter(price__lte=price_max)
                    products.extend(products_queryset.all())
            else:
                for sub_cate in sub_categories:
                    products.extend(sub_cate.products.all())
        else:
            taget_category = Category.objects.get(id = category_id, slug = category_slug)
            products = Product.objects.filter(category = taget_category)
            if price_min is not None and price_max is not None:
                products = products.filter(price__gte=price_min).filter(price__lte=price_max)

    else:
        query = request.GET.get('q')
        products = Product.objects.all().order_by('-created_at')
        if query:
            products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
            if price_min is not None and price_max is not None:
                products = products.filter(price__gte=price_min).filter(price__lte=price_max)

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(
        request, 
        f'{TEMPLATE_FOLDER_NAME}/product_list.html', 
        {
            'page_obj': page_obj, 
            'query': query,
            'categories_tree': categories_tree
        }
    )

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_detail(request: HttpRequest, id:int):
    try:
        product = get_object_or_404(
            Product.objects.prefetch_related('reviews__user'),
            id=id
        )

        rounded_mean_rating = round(product.mean_rating*100,1) if product.mean_rating is not None else None
        
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
