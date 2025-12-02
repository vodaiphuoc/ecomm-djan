from django import forms

from reviews.models import Review

class ReviewForm(forms.ModelForm):
    r"""Review form for users to write a product review"""
    class Meta:
        model = Review
        fields = ['content']

        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'content': 'Nội dung'
        }