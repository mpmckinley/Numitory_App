from django.contrib.auth.models import User
from django.db import models

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_desc = models.CharField(max_length=250)
    # image = models.ImageField(upload_to=)
    created = models.DateTimeField(auto_now_add=True)
    ACTIVE = 'A'
    SOLD = 'S'
    DISPOSED = 'D'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (SOLD, 'Sold'),
        (DISPOSED, 'Disposed'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey("inventory.Type", on_delete=models.RESTRICT)
    collection = models.ForeignKey("inventory.Collection", on_delete=models.RESTRICT)

    def __str__(self):
        return self.item_name + ' ->  ' + self.item_desc

class Type(models.Model):
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