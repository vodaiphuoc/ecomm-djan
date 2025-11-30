from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpRequest
from django.contrib.auth.forms import PasswordChangeForm

from e_commerce.forms import AppUserCreationForm

TEMPLATE_FOLDER_NAME = 'e_commerce'

def register(request: HttpRequest):
    if request.method == 'POST':
        form = AppUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect(f'/')
    else:
        form = AppUserCreationForm()
    
    return render(request, f'{TEMPLATE_FOLDER_NAME}/register.html', {'form': form})

class CustomLoginView(UserPassesTestMixin, LoginView):
    template_name = f'{TEMPLATE_FOLDER_NAME}/login.html'

    def test_func(self)->bool:
        r"""return True if the user is NOT authenticated"""
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        next_url = self.request.GET.get('next')

        if next_url:
            return redirect(next_url)
        
        return redirect(f'/')

class CustomPwdChangeView(PasswordChangeView):
    template_name = f'{TEMPLATE_FOLDER_NAME}/pwd_change.html'
    success_url= '/'
    form_class=PasswordChangeForm
    