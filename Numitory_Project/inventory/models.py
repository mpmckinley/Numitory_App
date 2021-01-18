from django.contrib.auth.models import User,AbstractUser,Group
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DecimalField, IntegerField
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
    new_id = ItemModel.objects.order_by("instance.item_name").last().id

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
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('WTB', 'WTB'),
        ('WTS', 'WTS'),
    ]
    GRADE_CHOICES = [
        ('Poor', 'P'),
        ('Fair', 'F'),
        ('About/Almost Good', 'AG'),
        ('Good', 'G'),
        ('Very Good', 'VG'),
        ('Fine', 'F'),
        ('Very Fine', 'VF'),
        ('Extremely Fine', 'EF'),
        ('About/Almost Uncirculated', 'AU'),
        ('Uncirculated/BU', 'BU'),
        ('Mint State', 'MS'),
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

    category = models.CharField("Category", max_length=20, choices=NUMI_CAT_CHOICES)
    classification = models.CharField("Classification", max_length=50, choices=CLASS_CHOICES)
    composition = models.CharField("Composition", max_length=50)
    country = models.CharField("Country", max_length=50, choices=COUNTRY_CHOICES, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    designer = models.CharField("Designer", max_length=250, blank=True, null=True)
    diameter = DecimalField("Diameter (mm)", max_digits=6, decimal_places=2, blank=True, null=True)
    edge = models.CharField("Edge", max_length=100, unique=True)
    face_value = MoneyField("Face Value", max_digits=5, decimal_places=3, default_currency='USD', blank=True, null=True)
    # ***face value currency from MoneyField
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, null=False)
    level1 = models.CharField("Level 1", max_length=100, unique=True, blank=True, null=True)
    level2 = models.CharField("Level 2", max_length=100, unique=True, blank=True, null=True)
    level3 = models.CharField("Level 3", max_length=100, unique=True, blank=True, null=True)
    level4 = models.CharField("Level 4", max_length=100, unique=True, blank=True, null=True)
    longname = models.CharField("Long Name", max_length=100, unique=True)
    mint = MultiSelectField(choices=MINT_CHOICES, blank=True, null=True)
    mintage = IntegerField("Mintage", blank=True, null=True)
    precious_purity = IntegerField("Precious Purity", blank=True, null=True)
    precious_type = IntegerField("Precious Type", blank=True, null=True)
    precious_weight = IntegerField("Precious Weight", blank=True, null=True)
    recycled = models.BooleanField(default=False)
    strike = models.CharField("Strike", max_length=20, blank=True, null=True)
    thickness = DecimalField("Thickness (mm)", max_digits=6, decimal_places=2, blank=True, null=True)
    type_desc = models.CharField("Description", max_length=250, blank=True, null=True)
    # type_name = models.CharField("Name", max_length=100, unique=True)
    type_img_obv = models.ImageField("", upload_to=upload_location, null=True, blank=True)
    type_img_rev = models.ImageField("", upload_to=upload_location, null=True, blank=True)
    url_ngc = models.URLField("NGC url", max_length=250, blank=True, null=True)
    url_other = models.URLField("Other url", max_length=250, blank=True, null=True)
    url_pcgs = models.URLField("PCGS url", max_length=250, blank=True, null=True)
    url_wiki = models.URLField("Wiki url", max_length=250, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    var_ngc = models.CharField("NGC #", max_length=100, unique=True, blank=True, null=True)
    var_pcgs = models.CharField("PCGS #", max_length=100, unique=True, blank=True, null=True)
    weight = models.CharField("Weight", max_length=10, blank=True, null=True)
    year_mint = models.CharField("Year | Mint", max_length=50, blank=True, null=True)


    def __str__(self):
        return self.longname

# class Type_Priv(models.Model):
#     # id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, null=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

# ***Second TYPE model that will hold non-GOVERNMENT issued types, bullion, etc.

#     # type_img_obv = models.ImageField("", upload_to=upload_location, null=True, blank=True)
#     # type_img_rev = models.ImageField("", upload_to=upload_location, null=True, blank=True)

#     def __str__(self):
#         return self.var_name


class Collection(models.Model):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, null=False)
    coll_name = models.CharField("Name", max_length=100, unique=True)
    coll_desc = models.CharField("Description", max_length=250)

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recycled = models.BooleanField(default=False)

    def __str__(self):
        return self.coll_name