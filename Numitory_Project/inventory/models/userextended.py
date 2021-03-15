from django.contrib.auth.models import Group, User
from django.db import models


def getGroupNames():
    try:
        groups = Group.objects.all().values_list('name', flat=True)
        id = Group.objects.all().values_list('id', flat=True)
        # print(zip(id, groups))
        return zip(id, groups)
    except:
        pass


class UserExtended(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(
        max_length=1,
        choices=getGroupNames(),
        blank=False,
        null=False
    )
