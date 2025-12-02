from django import forms

from orders.models import Order

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
