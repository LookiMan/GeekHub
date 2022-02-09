from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return f"Category: {self.name}"


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Product: {self.name}"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        verbose_name="количество", default=1)
