from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', )


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('mobile', 'national_id', 'medical_id')
