from celery import shared_task
from django.db.models import Avg
from .models import Review, Product

from .ml_service import get_predictor_instance
import uuid

@shared_task
def predict_ml_score(review_id: uuid.UUID, review_text: str):
    """
    Worker action: Takes the review text, predicts the score, 
    and then calls the next task to update the product.
    """
    try:
        # 1 get the instance
        predictor = get_predictor_instance()

        # 2 prediction
        predicted_score = predictor.forward(review_text)
        
        # 3. Update the Review instance with the predicted score
        Review.objects.filter(pk=review_id).update(score=predicted_score)

        # 4. Call the next task to calculate the new mean rating for the product
        rating_instance = Review.objects.get(pk=review_id)

        _update_product_mean_rating.delay(rating_instance.product_id)
        
    except Review.DoesNotExist:
        # Handle case where the rating might have been deleted while task was queued
        print(f"Rating with ID {review_id} not found.")


@shared_task
def _update_product_mean_rating(product_id:int):
    """
    Worker action: Recalculates the mean rating for the specified Product.
    """
    try:
        product = Product.objects.get(pk=product_id)
        
        # Calculate the mean based on the 'score' field
        average_result = product.reviews.exclude(score__isnull=True).aggregate(Avg('score'))
        
        # Update the Product and save
        product.mean_rating = average_result['score__avg']
        # Use update_fields
        product.save(update_fields=['mean_rating'])
        
    except Product.DoesNotExist:
        print(f"Product with ID {product_id} not found.")