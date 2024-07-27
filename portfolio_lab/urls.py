"""
URL configuration for portfolio_lab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.contrib.auth.views import LogoutView
from django.urls import path
from charity_donation.views import (LandingPageView, AddDonation, LoginView, RegisterView, LogoutView,
                                    ConfirmationView, ProfileView, DonationUpdateView, ProfileUpdateView)




urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', LandingPageView.as_view(), name='landing'),
    path('add_donation/', AddDonation.as_view(), name='add_donation'),
    path('form_confirmation/', ConfirmationView.as_view(), name='form_confirmation'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user_view/', ProfileView.as_view(), name='user_view'),
    path('user_update/', ProfileUpdateView.as_view(), name='user_update'),
    path('donation_update/<int:pk>', DonationUpdateView.as_view(), name='donation_update'),

]
