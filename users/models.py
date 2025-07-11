from django.contrib.auth.models import AbstractUser
from django.db import models
from autoslug import AutoSlugField

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(default='profile_images/default.png', upload_to='profile_images/')
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    acceptTerms=models.BooleanField(default=False)
    slug = AutoSlugField(populate_from='username', unique=True)

    USER_GROUPS = (
        ('admin', 'Admin'),
        ('mentor', 'Mentor'),
        ('author', 'Author'),
        ('consumer', 'Consumer'),
        ('manager', 'Manager'),
    )
    user_type = models.CharField(max_length=20, choices=USER_GROUPS, default='consumer')

    def __str__(self):
        return self.username if self.username else "Unknown User"
