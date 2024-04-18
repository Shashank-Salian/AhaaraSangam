from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Donors(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=100, null=False)
    contact_number = models.CharField(max_length=13, null=False)
    address = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state_iso2 = models.CharField(max_length=4, default=None)


class Donations(models.Model):
    donor = models.ForeignKey(Donors, on_delete=models.CASCADE)
    items = models.CharField(max_length=500, default='')
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='app_assets', null=True)

    FOOD_TYPE = [
        ("VEG", "Veg"),
        ("NON_VEG", "Non Veg"),
        ("BOTH", "Veg and Non Veg")
    ]
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE)