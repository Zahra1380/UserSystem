import random
import uuid
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import  TemplateView
from .forms import \
    (SignIn,
     RegisterForm,
     CheckOTP,
     SetInfo,
     UpdateUserForm,
     ForgetPasswordForm,
     ChangePasswordForm)

from .models import User, OTP
from django.urls import reverse, reverse_lazy
import ghasedakpack
from django.utils.timezone import timedelta, datetime
import shortuuid

SMS = ghasedakpack.Ghasedak("5b9b365a8ffd98979838487786ca83")

class home(TemplateView):
    template_name = 'account/home.html'


class SignInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('account:home'))
        form = SignIn()
        return render(request, 'account/sign_in.html', {'form': form})

    def post(self, request):
        form = SignIn(request.POST)
        if form.is_valid():
            print('is valid')
            cd = form.cleaned_data

            user = authenticate(phone_number=cd['username'], password=cd['password'])
            print(user)
            if not user:
                user = authenticate(username=cd['username'], password=cd['password'])
            print(user)
            # print(cd['password'].set_password())
            # print(User.objects.get(phone_number=cd['username'], u).password)
            if user:
                login(request, user)
                return redirect(reverse('account:home'))
            else:
                form.add_error('username', 'the phone number not exist')
        else:
            form.add_error('username', 'invalid data')

        return render(request, 'account/sign_in.html', {'form': form})


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('account:home'))


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            rand = random.randint(1000, 9999)

            SMS.verification({'receptor': cd["phone"], 'type': '1', 'template': 'rand', 'param1': rand})
            print(rand)
            token = uuid.uuid4()
            otp = OTP.objects.create(phone=cd['phone'], code=rand, token=token)
            print(rand)
            return redirect(reverse('account:checkotp') + f'?token={token}')
        else:
            form.add_error('phone', 'invalid date')
        return render(request, 'account/register.html', {'form': form})


class CheckOTPView(View):
    def get(self, request):
        form = CheckOTP()
        return render(request, 'account/check_otp.html', {'form': form})

    def post(self, request):
        form = CheckOTP(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            token = request.GET.get('token')
            if OTP.objects.filter(token=token, code=cd['code']).exists():
                otp = OTP.objects.get(token=token)
                if datetime.now(otp.expration_date.tzinfo) - otp.expration_date > timedelta(minutes=5):
                    form.add_error('code', 'code was intropt!')
                    otp.delete()
                    print('delete')
                else:
                    User.objects.create_user(phone_number=otp.phone)
                    return redirect(reverse('account:set-info') + f'?token={token}')
        else:
            form.add_error('code', 'invalid code')
        return render(request, 'account/check_otp.html', {'form': form})


class SetInfoView(View):
    def get(self, request):
        form = SetInfo()
        return render(request, 'account/set_info.html', {'form': form})

    def post(self, request):
        form = SetInfo(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            token = request.GET.get('token')
            otp = OTP.objects.get(token=token)

            user = User.objects.get(phone_number=otp.phone)
            user.set_password(cd['password1'])
            user.email = cd['email']
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            otp.delete()
            return redirect(reverse('account:home'))

        else:
            form.add_error('code', 'invalid code')
        return render(request, 'account/set_info.html', {'form': form})


def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            cd = user_form.cleaned_data
            user_form.save()
            return redirect(reverse('account:home'))

    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'account/profile.html', {'form': user_form})


class ForgetPassword(View):
    message = ''

    def get(self, request):
        form = ForgetPasswordForm()

        return render(request, 'account/forget_password.html', {'form': form, 'message': self.message})

    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            print('valid')
            try:
                phone = form.cleaned_data['phone_number']
                user = User.objects.get(phone_number=phone)
                rand = shortuuid.uuid()
                SMS.verification({'receptor': phone, 'type': '1', 'template': 'rand', 'param1': rand})
                print(rand)
                user.set_password(rand)
                user.save()
                self.message = ('your password change and send it to you from the sms!')
                return redirect(reverse_lazy('account:signin'))
            except:
                form.add_error('phone_number', 'this number does not exists')
        return render(request, 'account/forget_password.html', {'form': form, 'message': self.message})


class ChangePassword(View):
    def get(self, request):
        form = ChangePasswordForm()
        return render(request, 'account/change_password.html', {'form': form})

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print(self.request.user.phone_number)
            print(cd['old_password'])
            try:
                user = authenticate(username=self.request.user.phone_number, password=cd['old_password'])
                print(user)
                user.set_password(cd['password1'])
                user.save()
                return redirect(reverse('account:home'))

            except:
                form.add_error('old_password', 'your entry old password was wrong!')
        return render(request, 'account/change_password.html', {'form': form})

