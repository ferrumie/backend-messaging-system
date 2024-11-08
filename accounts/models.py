from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from accounts.manager import CustomUserManager

class User(AbstractBaseUser):
    """Model that represent user."""
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_datetime = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_datetime = models.DateTimeField(_('Last update at'), auto_now=True)

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    # Set custom user manager
    objects = CustomUserManager()

    def __str__(self) -> str:
        """Unicode representation of the user model."""
        return self.email
