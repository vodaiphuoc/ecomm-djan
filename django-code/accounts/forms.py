from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import AppUser

class AppUserCreationForm(UserCreationForm):

    avatar = forms.URLField(
        required=False, 
        help_text='Optional: Link to your profile picture.',
        label="Ảnh đại diện",
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    email = forms.EmailField(
        required=True,
                widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'username','email')

        labels = {
            'first_name': 'Tên',
            'last_name': 'Họ',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'password1' in self.fields:
            self.fields['password1'].label = 'Mật khẩu'
            
        if 'password2' in self.fields:
            self.fields['password2'].label = 'Xác nhận mật khẩu'
