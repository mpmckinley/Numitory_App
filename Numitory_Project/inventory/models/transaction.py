import json
from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from djmoney.models.fields import MoneyField
from django.utils.safestring import mark_safe


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

    @property
    def json_repr(self):
        return mark_safe(json.dumps(dict(
            date=self.date,
            tran_value=self.tran_value.amount,
            direction=self.direction,
            tran_quantity=self.tran_quantity
        ), cls=DjangoJSONEncoder))
