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
        institution_name = Institution.objects.all()

        return render(request, 'index.html', {'quantity': donation_sum, 'institutions': institution_count,
                                              'institution': institution_name})


class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {'categories': categories, 'institutions': institutions})

    def post(self, request):
        quantity = request.POST.get('quantity')
        category_ids = request.POST.getlist('categories')
        categories = Category.objects.filter(pk__in=category_ids)
        institution_id = request.POST.get('institution')
        institution = Institution.objects.get(pk=institution_id)
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')
        pick_up_date = request.POST.get('pick_up_date')
        pick_up_time = request.POST.get('pick_up_time')
        pick_up_comment = request.POST.get('pick_up_comment')
        user = request.user
        donation = Donation(quantity=quantity,
                            categories=categories,
                            institution=institution,
                            address=address,
                            phone_number=phone_number,
                            city=city,
                            zip_code=zip_code,
                            pick_up_date=pick_up_date,
                            pick_up_time=pick_up_time,
                            pick_up_comment=pick_up_comment,
                            user=user)
        donation.save()
        donation.categories.set(categories)
        return redirect('form-confirmation.html')


class ConfirmationView(View):
    def get(self, request):
        donation = Donation.objects.all()
        return render(request, 'form-confirmation.html')


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


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_view.html'
