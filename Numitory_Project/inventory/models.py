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



class MetalPrices(models.Model):
    gold_price=models.FloatField()
    silver_price=models.FloatField()
    platinum_price=models.FloatField()
    palladium_price=models.FloatField()
    updated_at=models.DateTimeField(auto_now_add=True)
    


class UserExtended(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    user_type=models.CharField(
        max_length=1, choices=getGroupNames(),
        blank=False, null=False)

class Item(models.Model):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, null=False)
    type = models.ForeignKey("inventory.Type", on_delete=models.RESTRICT)
    collection = models.ForeignKey("inventory.Collection", on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    condition = models.CharField(max_length=25, blank=True)
    graded = models.BooleanField(default=False)
    grade = models.CharField(max_length=6, blank=True)
    grader = models.CharField(max_length=5, blank=True, choices=GRADER_CHOICES)
    grader_id = models.CharField("ID#", max_length=50, blank=True)
    CAC = models.BooleanField(default=False)
    item_image = models.ImageField("", upload_to=upload_location, null=True, blank=True)
    mint = models.CharField("***MINT***", max_length=20, blank=True)

    def __str__(self):
        return self.item_name + ' ->  ' + self.item_desc

    @property
    def quantity(self):
        return Transaction.objects.filter(user=self.user, tran_item_id=self.id).aggregate(Sum('tran_quantity'))
    def value(self):
        return Transaction.objects.filter(user=self.user, tran_item_id=self.id).aggregate(Sum('tran_value'))

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

class Type(models.Model):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
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

    COUNTRY_CHOICES = [
        ('USA', 'USA'),
    ]

    country = models.CharField("Country", max_length=50, choices=COUNTRY_CHOICES)
    classification = models.CharField("Classification", max_length=50, choices=CLASS_CHOICES)
    category = models.CharField("Category", max_length=20, choices=NUMI_CAT_CHOICES)
    type_name = models.CharField("Name", max_length=100, unique=True)
    type_desc = models.CharField("Description", max_length=250)
    type_dates = models.CharField("Dates", max_length=250)
    mints = MultiSelectField(choices=MINT_CHOICES, blank=True, null=True)
    face_value = MoneyField("Face Value", max_digits=5, decimal_places=3, default_currency='USD',)
    url_pcgs = models.CharField("PCGS url", max_length=250, blank=True, null=True)
    url_ngc = models.CharField("NGC url", max_length=250, blank=True, null=True)
    url_other = models.CharField("Other url", max_length=250, blank=True, null=True)
    # type_img_obv = models.ImageField("", upload_to=upload_location, null=True, blank=True)
    # type_img_rev = models.ImageField("", upload_to=upload_location, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.type_name

class Type_Detl(models.Model):
    type = models.ForeignKey("inventory.Type", on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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

    var_name = models.CharField(max_length=50)
    var_desc = models.CharField(max_length=50)
    year = models.IntegerField("Year")
    mint = MultiSelectField(choices=MINT_CHOICES, blank=True, null=True)
    comp = models.CharField("Composition", max_length=50)
    weight = models.DecimalField("Weight (ozT)", max_digits=10, decimal_places=4)
    precious_type = models.CharField(max_length=10, choices=METAL_CHOICES)
    precious_purity = models.DecimalField("Precious Purity", max_digits=4, decimal_places=4)
    precious_weight = models.DecimalField("Precious Weight (ozT)", max_digits=10, decimal_places=4)
    edge = models.CharField(max_length=50)
    mintage = models.IntegerField("Mintage")
    url_ngc = models.CharField("NGC url", max_length=250, blank=True, null=True)
    url_other = models.CharField("Other url", max_length=250, blank=True, null=True)
    url_pcgs = models.CharField("PCGS url", max_length=250, blank=True, null=True)
    designer = models.CharField(max_length=30, blank=True, null=True)
    recycled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    # type_img_obv = models.ImageField("", upload_to=upload_location, null=True, blank=True)
    # type_img_rev = models.ImageField("", upload_to=upload_location, null=True, blank=True)

    def __str__(self):
        return self.var_name


class Collection(models.Model):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, null=False)
    coll_name = models.CharField("Name", max_length=100, unique=True)
    coll_desc = models.CharField("Description", max_length=250)

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recycled = models.BooleanField(default=False)

    def __str__(self):
        return self.coll_name