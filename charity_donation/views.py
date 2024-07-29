from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date, parse_time
from django.views import View
from django.views.generic import TemplateView

from charity_donation.forms import DonationForm, UserUpdateForm
from charity_donation.models import Donation, Institution, Category


class LandingPageView(View):
    def get(self, request):
        donations = Donation.objects.all()
        donation_sum = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        institutions = donations.values('institution').distinct()
        institution_count = institutions.count()
        return render(request, 'index.html', {'quantity': donation_sum, 'institutions': institution_count})


class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        donation_view = Donation.objects.filter(user=request.user).order_by('-id').first()
        return render(request, 'form.html', {'categories': categories, 'institutions': institutions, 'donation_view': donation_view})

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
        pick_up_date = parse_date(request.POST.get('pick_up_date'))
        pick_up_time = parse_time(request.POST.get('pick_up_time'))
        pick_up_comment = request.POST.get('pick_up_comment')
        is_taken = request.POST.get('is_taken') == 'on'
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
                            user=user,
                            is_taken=is_taken)
        donation.save()
        donation.categories.set(categories)

        return redirect('form_confirmation')


class ConfirmationView(View):
    def get(self, request):
        donation = Donation.objects.filter(user=request.user).order_by('-id').first()
        return render(request, 'form-confirmation.html', {'donation': donation})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donations'] = [(donation, DonationForm(instance=donation))
                                for donation in Donation.objects.filter
                                (user=self.request.user).order_by('is_taken')]
        return context


class DonationUpdateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        donation = Donation.objects.get(id=kwargs['pk'])
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            updated_donation = form.save()
            if updated_donation.is_taken:
                updated_donation.is_archived = True
                updated_donation.save()
        return redirect('user_view')


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        profile_form = UserUpdateForm(instance=user)
        password_form = PasswordChangeForm(user=user, use_required_attribute=False)
        return render(request, 'user_update.html', {'profile_form': profile_form,
                                                    'password_form': password_form})

    def post(self, request):
        user = request.user
        profile_form = UserUpdateForm(request.POST, instance=user)
        password_form = PasswordChangeForm(user=user, data=request.POST)

        if profile_form.is_valid() and (not password_form.is_bound or password_form.is_valid()):
            if password_form.is_bound and password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, 'Your password was successfully updated!')

            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('user_view')

        return render(request, 'user_update.html', {'profile_form': profile_form,
                                                    'password_form': password_form})


