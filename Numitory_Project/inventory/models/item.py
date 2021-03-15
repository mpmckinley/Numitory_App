import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

from ..helpers import upload_location
from .transaction import Transaction


class Item(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('WTB', 'WTB'),
        ('WTS', 'WTS'),
    ]
    GRADE_CHOICES = [
        ('P', 'P'),
        ('F', 'F'),
        ('AG', 'AG'),
        ('G', 'G'),
        ('VG', 'VG'),
        ('F', 'F'),
        ('VF', 'VF'),
        ('EF', 'EF'),
        ('AU', 'AU'),
        ('BU', 'BU'),
        ('MS', 'MS'),
    ]
    GRADER_CHOICES = [
        ('PCGS', 'PCGS'),
        ('NGC', 'NGC'),
        ('ANACS', 'ANACS'),
        ('Other', 'Other'),
    ]

    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, null=False)
    type = models.ForeignKey('inventory.Type', on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    item_name = models.CharField("Name", max_length=50, null=True, blank=True)
    item_desc = models.TextField("Description / Notes", max_length=250)
    item_image = models.ImageField("", upload_to=upload_location, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    graded = models.BooleanField(default=False)
    grade = models.CharField(max_length=25, choices=GRADE_CHOICES, null=True, blank=True)
    grade_num = models.CharField(max_length=6, null=True, blank=True)
    grader = models.CharField(max_length=5, null=True, blank=True, choices=GRADER_CHOICES)
    grader_id = models.CharField("ID#", max_length=50, null=True, blank=True)
    details = models.BooleanField(default=False)
    CAC = models.BooleanField(default=False)
    mint = models.CharField("***MINT***", max_length=20, null=True, blank=True)
    type = models.ForeignKey("inventory.Type", on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True)
    condition = models.CharField(max_length=25, null=True, blank=True)
    # year = models.IntegerField(null=True, blank=True)
    collection = models.ForeignKey("inventory.Collection", on_delete=models.RESTRICT)
    count = models.IntegerField(default='1')

    def __str__(self):
        return self.item_name + ' ->  ' + self.item_desc

    @property
    def quantity(self):
        return Transaction.objects.filter(user=self.user, tran_item_id=self.id).aggregate(Sum('tran_quantity'))

    def value(self):
        return Transaction.objects.filter(user=self.user, tran_item_id=self.id).aggregate(Sum('tran_value'))
    # ***Direct links to grader verification pages:
    # def pcgs(self):
    #     return https://www.pcgs.com/cert/{{ grader_id }}
    # def ngc(self):
    #     return https://www.ngccoin.com/certlookup/{{ grader_id}}/{{ grade_num }}
