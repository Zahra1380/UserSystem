import time

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager

class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:blog_detail', args=[self.email])

class OTP(models.Model):
    token = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    expration_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.phone

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='addresess')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(blank= True, null=True)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=300)
    postal_code= models.CharField(max_length=30)


    def __str__(self):
        return self.user.phone
