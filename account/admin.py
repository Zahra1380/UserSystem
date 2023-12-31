from .forms import UserCreationForm, UserChangeForm
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.models import User, OTP, UserAddress


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm


    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["phone_number", "email", "is_admin", "is_active"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["phone_number", "password", 'email']}),
        ("اطلاعات شخصی", {"fields": ["full_name"]}),
        ("دسترسی ها", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone_number", "full_name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["phone_number"]
    ordering = ["phone_number"]
    filter_horizontal = []


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone']

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.register(OTP)