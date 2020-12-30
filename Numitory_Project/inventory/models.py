from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_desc = models.CharField(max_length=250)
    # image = models.ImageField(upload_to=)
    created = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    #Attributes
    graded = models.BooleanField(default=False)
    grade = models.CharField(max_length=6, blank=True)
    condition = models.CharField(max_length=25, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey("inventory.Type", on_delete=models.RESTRICT)
    collection = models.ForeignKey("inventory.Collection", on_delete=models.RESTRICT)

    def __str__(self):
        return self.item_name + ' ->  ' + self.item_desc

class Transaction(models.Model):
    DIR_CHOICES = [
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
        ('Trade', 'Trade'),
    ]

    direction = models.CharField(max_length=10, choices=DIR_CHOICES)
    tran_quantity = models.IntegerField()
    tran_value = models.DecimalField(max_digits=50, decimal_places=2)
    date = models.DateField()

    tran_item = models.ForeignKey("inventory.Item", on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Type(models.Model):
    type_name = models.CharField(max_length=100, unique=True)
    type_desc = models.CharField(max_length=250)
    
    CAT_CHOICES = [
        ('Bullion', 'Bullion'),
        ('Numi', 'Numi'),
        ('Other', 'Other'),
    ]
    METAL_CHOICES = [
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
        ('Palladium', 'Palladium'),
    ]

    category = models.CharField(max_length=10, choices=CAT_CHOICES)
    metal = models.CharField(max_length=10, choices=METAL_CHOICES)
    metal_weight = models.DecimalField(max_digits=10, decimal_places=4)
    purity = models.DecimalField(max_digits=5, decimal_places=4)
    
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recycled = models.BooleanField(default=False)

    def __str__(self):
        return self.type_name

class Collection(models.Model):
    coll_name = models.CharField(max_length=100, unique=True)
    coll_desc = models.CharField(max_length=250)

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recycled = models.BooleanField(default=False)

    def __str__(self):
        return self.coll_name