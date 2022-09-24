from PIL import Image

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

MALE = "MALE"
FEMALE = "FEMALE"
NONE = "NONE"

GENDER_CHOICES = (
    (MALE, "Male"),
    (FEMALE, "Female"),
    (NONE, "None")
)

class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
    auth_token = models.CharField(max_length=100, unique=True)
    hash = models.CharField(max_length=36, unique=True)
    image = models.ImageField(upload_to='uploads/profile/', default='profile.png')
    photo = models.ImageField(upload_to='uploads/profile/compressed/', default='profile.png')
    is_online = models.BooleanField(default=False)
    bio = models.TextField(max_length=250, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, default=NONE)
    location = models.CharField(max_length=50, blank=True)

    REQUIRED_FIELDS = [
   	 'email',
    ]

    def __str__(self):
        return self.email