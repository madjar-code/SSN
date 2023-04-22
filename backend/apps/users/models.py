from __future__ import annotations
from enum import Enum
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from common.mixins.models import UUIDModel


class ErrorMessages(Enum):
    NO_EMAIL = 'Users must have an email address'
    NO_NAME = 'Users must have names'
    NO_PASSWORD = 'Password is required'


class UserManager(BaseUserManager):
    """Helps Django work with our custom user model"""
    use_in_migrations = True
    
    def create_user(self, name: str, email: str,
                    password: str = None) -> User:
        """Creates a new user profile objects"""
        if not email:
            raise ValueError(ErrorMessages.NO_EMAIL.value)

        if not name:
            raise ValueError(ErrorMessages.NO_NAME.value)

        email = self.normalize_email(email)
        name = name.strip()
        user: User = self.model(name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str = None) -> User:
        if not password:
            raise ValueError(ErrorMessages.NO_PASSWORD.value)
        user: User = self.create_user('admin', email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(UUIDModel, AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.URLField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self) -> str:
        return self.email
