from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        users = self.model(email=email, **extra_fields)
        users.set_password(password)
        users.save(using=self.db)
        return users

    def create_user(self, email, password, **extra_fields):
        if not email:
            return ValueError('Email must be set!')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(email, password, extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)
