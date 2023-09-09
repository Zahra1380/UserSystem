from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        """
        Creates and saves a User with the given phone_number and password.
        """
        if not phone_number:
            raise ValueError("Users must have an phone number")

        user = self.model( phone_number=phone_number,)

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, phone_number, email, full_name, password=None):
        """
        Creates and saves a superuser with the given phone_number and password.
        """
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            email=email,
            full_name=full_name
        )
        user.is_admin = True
        user.save(using=self._db)
        return user