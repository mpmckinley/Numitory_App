from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    DIR_CHOICES = [
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
        ('Trade', 'Trade'),
    ]

    tran_item = models.ForeignKey("inventory.Item", on_delete=models.CASCADE)
    direction = models.CharField(max_length=10, choices=DIR_CHOICES,)
    tran_quantity = models.IntegerField("Quantity")
    date = models.DateField()
    tran_value = MoneyField("***VALUE***", max_digits=50, decimal_places=2, default_currency='USD',)
    #tran_value_currency is auto from MoneyField
    created = models.DateTimeField(auto_now_add=True)
