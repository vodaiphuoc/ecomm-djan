from django.db import models
import uuid

################## Category and Product ##################
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,               
        blank=True,              
        related_name='children',
    )

    class Meta:
        ordering = ['name']
        unique_together = ('slug', 'parent',) 
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    r"""
    Schema for product table
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name="products")
    description = models.TextField(blank=True)
    brand_name = models.CharField(max_length=100)
    price = models.IntegerField()
    stock = models.IntegerField()
    is_active = models.BooleanField()
    thumbnail_url = models.URLField(null= False)
    mean_rating = models.FloatField(null= True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductImg(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name = "images")
    image_url = models.URLField(null= False)
    created_at = models.DateTimeField(auto_now_add=True)

