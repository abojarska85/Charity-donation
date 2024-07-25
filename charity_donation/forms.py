from django import forms

from charity_donation.models import Donation


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['is_taken']