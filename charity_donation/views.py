from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from charity_donation.models import Donation


class LandingPageView(View):
    def get(self, request):
        donations = Donation.objects.all()
        donation_sum = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        institutions = donations.values('institution').distinct()
        institution_count = institutions.count()
        return render(request, 'index.html', {'quantity': donation_sum, 'institution': institution_count})


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')