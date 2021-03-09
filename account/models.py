import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core import validators
from django.db import models, transaction
from django.utils import timezone
from django.utils.crypto import get_random_string


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email, username and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.generate_activation_code()
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(db_index=True, max_length=50, unique=True)
    email = models.EmailField(unique=True, validators=[validators.validate_email])
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to="users", blank=True, null=True)
    activation_code = models.CharField(max_length=36, blank=True)
    last_activity = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def generate_activation_code(self):
        code = str(uuid.uuid4())
        self.activation_code = code
        self.save()

    def generate_password_reset_code(self):
        code = get_random_string(length=6, allowed_chars="0123456789")
        self.activation_code = code
        self.save()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
