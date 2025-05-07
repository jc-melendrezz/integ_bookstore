from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

    on_sale = models.BooleanField(default=False)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sale_start = models.DateTimeField(null=True, blank=True)
    sale_end = models.DateTimeField(null=True, blank=True)

    def current_price(self):
        now = timezone.now()
        if self.on_sale and self.sale_start and self.sale_end:
            if self.sale_start <= now <= self.sale_end:
                if self.discount_percentage:
                    discount = self.price*(self.discount_percentage/100)
                    return self.price - discount
        return self.price

    @property
    def calculated_discount_percentage(self):
        # Calculates based on actual discounted price
        now = timezone.now()
        if self.on_sale and self.discount_percentage and self.sale_start and self.sale_end:
            if self.sale_start <= now <= self.sale_end:
                return int(self.discount_percentage)
        return 0

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  # e.g., Pending, Completed
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Price at the time of purchase

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

