from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AppUser, Order, Review

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

class AppUserChangeForm(UserChangeForm):
    avatar = forms.URLField(
        required=False, 
        help_text='Optional: Link to your profile picture.',
        label="Ảnh đại diện",
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = AppUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

class OrderForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150, 
        label= "Tên",
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    last_name = forms.CharField(
        max_length=150, 
        label= "Họ",
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    email = forms.EmailField(
        max_length=254, 
        label= "Email",
        help_text= "Email đã đăng ký",
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = Order
        fields = ['phone_number', 'address']
        
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'phone_number': 'Số  điện thoại',
            'address': 'Địa chỉ'
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']

        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'content': 'Nội dung'
        }