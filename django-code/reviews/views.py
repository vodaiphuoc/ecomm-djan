from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.http import HttpRequest
from django.db import transaction
from django.contrib import messages

from reviews.forms import ReviewForm
from reviews.models import Review
from products.models import Product

TEMPLATE_FOLDER_NAME = 'reviews'

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
                return redirect('products:product_detail', id=product_id)

        except Product.DoesNotExist:
            messages.error(request, "Sản phẩm không tồn tại")
            return redirect('products:product_list')

        except Exception as e:
            messages.error(request, "Lỗi server")
            return redirect('products:product_detail', id=product_id)

    else:
        messages.error(request, "Lỗi form")
        return redirect('products:product_detail', id=product_id)
