from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import uuid
from .utils import get_avatar_color

################## User ##################
# dont need to use Role table!
class AppUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        editable=False
    )
    
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False
    )

    avatar = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_initial(self):
        return self.username[0].upper()

    @property
    def get_avatar_color(self)->str:
        """
        Gets a consistent background color for the letter avatar.
        We use the UUID as the unique identifier for hashing.
        """
        # Assuming 'id' is your UUIDField as per your model screenshot
        return get_avatar_color(self.id)

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

################## Order and Oder item ##################
class Order(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="orders")
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'\d{10}$',
                message="Phone number must have 15 digits"
            )
        ],
        help_text="Số điện thoại liên hệ"
    )
    address = models.CharField(max_length=250, help_text= "Địa chỉ cần giao")
    
    payment_status = models.CharField(
        max_length=7,
        choices=[('FAILED','FAILED'), ('PENDING','PENDING'), ('SUCCESS','SUCCESS')],
        default='PENDING'
    )
    total_cost = models.IntegerField()

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