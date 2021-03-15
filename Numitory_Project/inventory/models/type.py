import uuid
from django.db import models
from django.db.models.fields import DecimalField, IntegerField
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

from ..helpers import upload_location


class Type(models.Model):
    CLASS_CHOICES = [
        ('Government', 'Government'),
        ('Private', 'Private'),
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
    edge = models.CharField("Edge", max_length=100, blank=True, null=True)
    face_value = DecimalField("Face Value", max_digits=5, decimal_places=3, blank=True, null=True)
    face_value_currency = models.CharField("Currency", max_length=100, blank=True, null=True)
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, null=False)
    level1 = models.CharField("Level 1", max_length=100, blank=True, null=True)
    level2 = models.CharField("Level 2", max_length=100, blank=True, null=True)
    level3 = models.CharField("Level 3", max_length=100, blank=True, null=True)
    level4 = models.CharField("Level 4", max_length=100, blank=True, null=True)
    level5 = models.CharField("Level 5", max_length=100, blank=True, null=True)
    longname = models.CharField("Long Name", max_length=100, unique=True)
    mint = MultiSelectField(choices=MINT_CHOICES, blank=True, null=True)
    mintage = IntegerField("Mintage", blank=True, null=True)
    obv_desc = models.CharField("Obverse Desc.", max_length=100, blank=True, null=True)
    precious_purity = IntegerField("Precious Purity", blank=True, null=True)
    precious_type = IntegerField("Precious Type", blank=True, null=True)
    precious_weight_g = IntegerField("Precious Weight (g)", blank=True, null=True)
    precious_weight_ozt = IntegerField("Precious Weight (ozt)", blank=True, null=True)
    recycled = models.BooleanField(default=False)
    refiner = models.CharField("Refiner", max_length=50, blank=True, null=True)
    rev_desc = models.CharField("Reverse Desc.", max_length=100, blank=True, null=True)
    serials = models.CharField("Serials", max_length=100, blank=True, null=True)
    strike = models.CharField("Strike", max_length=20, blank=True, null=True)
    thickness = DecimalField("Thickness (mm)", max_digits=6, decimal_places=2, blank=True, null=True)
    type_desc = models.CharField("Description", max_length=250, blank=True, null=True)
    type_img_obv = models.ImageField("", upload_to=upload_location, null=True, blank=True)
    type_img_rev = models.ImageField("", upload_to=upload_location, null=True, blank=True)
    url_ngc = models.URLField("NGC url", max_length=250, blank=True, null=True)
    url_other = models.URLField("Other url", max_length=250, blank=True, null=True)
    url_pcgs = models.URLField("PCGS url", max_length=250, blank=True, null=True)
    url_wiki = models.URLField("Wiki url", max_length=250, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    var_ngc = models.CharField("NGC #", max_length=100, blank=True, null=True)
    var_pcgs = models.CharField("PCGS #", max_length=100, blank=True, null=True)
    weight = models.CharField("Weight", max_length=10, blank=True, null=True)
    year_mint = models.CharField("Year | Mint", max_length=50, blank=True, null=True)

    def __str__(self):
        return self.longname
