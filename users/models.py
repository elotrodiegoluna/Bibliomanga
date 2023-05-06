from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import MyUserManager


class User(AbstractBaseUser):
    email = models.EmailField(max_length=64,unique=True,)
    username = models.CharField(max_length=64, unique=True,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin