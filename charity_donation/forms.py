from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from charity_donation.models import Donation


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['is_taken']


class UserUpdateForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput,
                                       help_text='Please enter current password.',
                                       required=False)


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'current_password']

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if current_password and not self.instance.check_password(current_password):
            raise forms.ValidationError('Current password does not match.')
        return current_password

