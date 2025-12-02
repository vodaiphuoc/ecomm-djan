from django.db import models
import uuid

from products.models import Product
from accounts.models import AppUser

class Review(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name="reviews")
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    content = models.TextField()
    score = models.BooleanField(null=True, default=None) # True for positive, False for negative
    created_at = models.DateTimeField(auto_now_add=True)