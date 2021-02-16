import uuid
from django.db import models
from django.contrib.auth.models import User


class Collection(models.Model):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, null=False)
    coll_name = models.CharField("Name", max_length=100, unique=True)
    coll_desc = models.CharField("Description", max_length=250)

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recycled = models.BooleanField(default=False)

    def __str__(self):
        return self.coll_name
