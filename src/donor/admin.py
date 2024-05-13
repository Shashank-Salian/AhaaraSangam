from django.contrib import admin
from donor.models import Donations, Donors

# Register your models here.
admin.site.register(Donors)
admin.site.register(Donations)
