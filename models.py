from django.contrib.auth.models import User,AbstractUser,Group
from django.db import models
from django.db.models.deletion import CASCADE
from djmoney.models.fields import MoneyField
from multiselectfield import MultiSelectField
from django.db.models import Sum
import uuid

# User._meta.get_field('email')._unique = True
# User._meta.get_field('email').blank = False
# User._meta.get_field('email').null = False

def upload_location(instance, filename):
    filebase, extension = filename.split(".")
    return "%s/%s.%s" %(instance.item_name, instance.item_name, extension)
    ItemModel = instance.__class__
    new_id = ItemModel.objects.order_by("instance.item_name").last().id + 1

    return "%s" %(filename)

def getGroupNames():
    groups = Group.objects.all().values_list('name', flat=True)
    id = Group.objects.all().values_list('id', flat=True)
    # print(zip(id, groups))
    return zip(id, groups)    

class UserExtended(models.Model):
    # id=models.AutoField(primary_key=True)
    # user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    user_type=models.CharField(
        max_length=1, choices=getGroupNames(),
        blank=False, null=False)

class Item(models.Model):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, null=False)
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('WTB', 'WTB'),
        ('WTS', 'WTS'),
    ]
    GRADER_CHOICES = [
        ('PCGS', 'PCGS'),
        ('NGC', 'NGC'),
        ('ANACS', 'ANACS'),
        ('Other', 'Other'),
    ]

    item_name = models.CharField("Name", max_length=50, null=True, blank=True)
    item_desc = models.TextField("Description / Notes", max_length=250)
    item_image = models.ImageField("", upload_to=upload_location, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    
    #Attributes
    graded = models.BooleanField(default=False)
    grader = models.CharField(max_length=5, blank=True, choices=GRADER_CHOICES)
    grader_id = models.CharField("ID#", max_length=50, blank=True)
    grade = models.CharField(max_length=6, blank=True)
    CAC = models.BooleanField(default=False)
    condition = models.CharField(max_length=25, blank=True)
    mint = models.CharField("***MINT***", max_length=20, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    type = models.ForeignKey("inventory.Type", on_delete=models.CASCADE)
    collection = models.ForeignKey("inventory.Collection", on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name + ' ->  ' + self.item_desc

    @property
    def quantity(self):
        return Transaction.objects.filter(user=self.user, tran_item_id=self.id).aggregate(Sum('tran_quantity'))
    def value(self):
        return Transaction.objects.filter(user=self.user, tran_item_id=self.id).aggregate(Sum('tran_value'))
    # def count(self):
    #     return Item.objects.filter(user=self.user, status='Active').aggregate(Count('id'))

class Transaction(models.Model):
    DIR_CHOICES = [
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
        ('Trade', 'Trade'),
    ]

    date = models.DateField()
    direction = models.CharField(
        max_length=10,
        choices=DIR_CHOICES,
    )
    tran_quantity = models.IntegerField("Quantity")
    tran_value = MoneyField(
        "***VALUE***",
        max_digits=50,
        decimal_places=2,
        default_currency='USD',
    )

    created = models.DateTimeField(auto_now_add=True)
    tran_item = models.ForeignKey("inventory.Item", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Type(models.Model):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, null=False)
    
    CLASS_CHOICES = [
        ('Bullion', 'Bullion'),
        ('Numismatic', 'Numismatic'),
        ('Other', 'Other'),
    ]
    NUMI_CAT_CHOICES = [
        ('Half-Cents', 'Half-Cents'),
        ('Cents', 'Cents'),
        ('Two Cents', 'Two Cents'),
        ('Three Cents', 'Three Cents'),
        ('Nickels', 'Nickels'),
        ('Half-Dimes', 'Half-Dimes'),
        ('Dimes', 'Dimes'),
        ('Quarters', 'Quarters'),
        ('Half Dollars', 'Half Dollars'),
        ('Dollars', 'Dollars'),
        ('Gold Coins', 'Gold Coins'),
        ('Commemoratives', 'Commemoratives'),
        ('Bullion Coins', 'Bullion Coins'),
        ('Proof & Mint Sets', 'Proof & Mint Sets'),
        ('Colonials', 'Colonials'),
        ('Territorial', 'Territorial'),
        ('Patterns', 'Patterns'),
        ('Other', 'Other'),
    ]
    METAL_CHOICES = [
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
        ('Palladium', 'Palladium'),
    ]
    MINT_CHOICES = [
        ('N/A', 'N/A'),
        ('Philadelphia', 'Philadelphia'),
        ('Charlotte', 'Charlotte'),
        ('Dahlonega', 'Dahlonega'),
        ('New Orleans', 'New Orleans'),
        ('Carson City', 'Carson City'),
        ('San Francisco', 'San Francisco'),
        ('Denver', 'Denver'),
        ('West Point', 'West Point'),
        ('Manila', 'Manila'),
    ]

    type_name = models.CharField("Name", max_length=100, unique=True)
    type_desc = models.CharField("Description", max_length=250)
    classification = models.CharField(max_length=10, choices=CLASS_CHOICES)
    
    category = models.CharField("Category", max_length=20, choices=NUMI_CAT_CHOICES)
    metal = models.CharField(max_length=10, choices=METAL_CHOICES)
    metal_weight = models.DecimalField("Metal Weight (ozT)", max_digits=10, decimal_places=4)
    purity = models.DecimalField(max_digits=5, decimal_places=4)
    mint = MultiSelectField(choices=MINT_CHOICES, blank=True, null=True)
    designer = models.CharField(max_length=30, blank=True, null=True)
    coin_weight = models.DecimalField("Coin Weight (g)", max_digits=10, decimal_places=2, blank=True, null=True)
    face_value = MoneyField(
        "Face Value",
        max_digits=5,
        decimal_places=3,
        default_currency='USD',
    )

    url_pcgs = models.CharField("PCGS url", max_length=250, blank=True, null=True)
    url_ngc = models.CharField("NGC url", max_length=250, blank=True, null=True)
    url_other = models.CharField("Other url", max_length=250, blank=True, null=True)

    recycled = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.type_name

class Collection(models.Model):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, null=False)
    coll_name = models.CharField("Name", max_length=100, unique=True)
    coll_desc = models.CharField("Description", max_length=250)

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recycled = models.BooleanField(default=False)

    def __str__(self):
        return self.coll_name