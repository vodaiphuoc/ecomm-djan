from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid

################## User ##################
# dont need to use Role table!
class AppUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    fullname = models.CharField(max_length=50)
    avatar = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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

class Product(models.Model):
    r"""
    Schema for product table
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    description = models.TextField(blank=True)
    brand_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
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

################## Order and Oder item ##################
class Order(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    address = models.CharField(max_length=250)
    
    payment_status = models.CharField(
        max_length=7,
        choices=[('FAILED','FAILED'), ('PENDING','PENDING'), ('SUCCESS','SUCCESS')],
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.product.price * self.quantity

################## Review ##################
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