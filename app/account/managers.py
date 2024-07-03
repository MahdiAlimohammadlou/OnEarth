from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password, phone_number):
        if not phone_number:
            raise ValueError("User must have a phone number")
        
        if not email:
            raise ValueError("User must have an email")
        
        user = self.model(email=email, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, phone_number):
        user = self.create_user(email, password, phone_number)
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_user_with_email_only(self, email):
        if not email:
            raise ValueError("User must have an email")
        user = self.model(email=email)
        user.set_unusable_password()
        user.save(using=self._db)
        return user

