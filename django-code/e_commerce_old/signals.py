from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review

from .tasks import predict_ml_score

@receiver(post_save, sender=Review)
def update_product_mean_rating(sender, instance: Review, created, **kwargs):
    r"""
    Signal handler to update the Product's mean rating when a create Review is created.
    """
    if created:
        predict_ml_score.delay(instance.id, instance.content)