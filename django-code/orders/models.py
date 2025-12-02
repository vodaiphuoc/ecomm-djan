from django.db import models
from django.core.validators import RegexValidator

from accounts.models import AppUser
from products.models import Product

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
