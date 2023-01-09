from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Portfolio(models.Model):
    stock = models.CharField(max_length=100)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    cur_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.SmallIntegerField()
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    date_purchased = models.DateField(auto_now_add=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ['date_purchased']

    def __str__(self):
        return self.stock

class Cash(models.Model):
    cash = models.DecimalField(max_digits=7, decimal_places=2, default=10000)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    class Meta:
        ordering = ['cash']

    def __str__(self):
        return str(self.cash)