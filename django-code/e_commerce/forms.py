from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AppUser

class AppUserCreationForm(UserCreationForm):
    fullname = forms.CharField(max_length=50, help_text='Enter your full name.')
    avatar = forms.URLField(required=False, help_text='Optional: Link to your profile picture.')

    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = UserCreationForm.Meta.fields + ('fullname', 'avatar',)

class AppUserChangeForm(UserChangeForm):
    class Meta:
        model = AppUser
        fields = ('fullname', 'avatar', 'email', 'password') # Example fields for user change