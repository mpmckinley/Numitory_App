from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s.%s" %(instance.item_name, instance.item_name, extension)
    ItemModel = instance.__class__
    new_id = ItemModel.objects.order_by("instance.item_name").last().id + 1

    return "%s" %(filename)

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_desc = models.CharField(max_length=250)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
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
    CAT_CHOICES = [
        ('Bullion', 'Bullion'),
        ('Numi', 'Numi'),
        ('Other', 'Other'),
    ]
    category = models.CharField(max_length=10, choices=CAT_CHOICES)
    type_name = models.CharField(max_length=100, unique=True)
    type_desc = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recycled = models.BooleanField(default=False)

    def __str__(self):
        return self.type_name


class Collection(models.Model):
    coll_name = models.CharField(max_length=100, unique=True)
    coll_desc = models.CharField(max_length=250)
    recycled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.coll_name