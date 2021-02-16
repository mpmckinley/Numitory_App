from django.db import models


class MetalPrices(models.Model):
    gold_price = models.FloatField()
    silver_price = models.FloatField()
    platinum_price = models.FloatField()
    palladium_price = models.FloatField()
    updated_at = models.DateField(auto_now_add=True)
