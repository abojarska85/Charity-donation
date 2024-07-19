from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from charity_donation.models import Donation, Institution, Category


class LandingPageView(View):
    def get(self, request):
        donations = Donation.objects.all()
        donation_sum = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        institutions = donations.values('institution').distinct()
        institution_count = institutions.count()
        # institution_name = Institution.objects.all()

        return render(request, 'index.html', {'quantity': donation_sum, 'institutions': institution_count})



class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {'categories': categories, 'institutions': institutions})


    def post(self, request):
        quantity = request.POST.get('quantity')
        donation = Donation(quantity=quantity)
        donation.save()
        return redirect('add_donation')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            redirect_url = request.POST.get('next', 'landing')
            return redirect(redirect_url)
        else:
            return redirect('register')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing')



class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        if password != "" and password == password2:
            u = User(username=email, first_name=name, last_name=surname, email=email)
            u.set_password(password)
            u.save()
            return redirect('login')
        return render(request, 'register.html', {'error': 'Passwords do not match'})