from django.contrib import admin

from charity_donation.models import Donation, Category, Institution

admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(Institution)
