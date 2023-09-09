from django.urls import path
from . import views
app_name = 'account'

urlpatterns = [
    path('home/', views.home.as_view(), name='home'),
    path('sign-in/', views.SignInView.as_view(), name='signin'),
    path('log-out/', views.LogOutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('checkotp/', views.CheckOTPView.as_view(), name='checkotp'),
    path('set-info/', views.SetInfoView.as_view(), name='set-info'),
    path('profile/', views.profile, name='profile'),
    path('forget_password/', views.ForgetPassword.as_view(), name='forget_password'),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),
]