from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import CustomLoginView, CustomPwdChangeView, register

app_name = 'accounts'

urlpatterns = [
    path('login', CustomLoginView.as_view(),name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='/'),name='logout'),
    path('register', register, name='register'),
    path('pwd_change', CustomPwdChangeView.as_view(),name='pwd_change'),
]
