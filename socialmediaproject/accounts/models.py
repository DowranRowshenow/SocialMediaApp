from django.db import models
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
    image = models.ImageField(upload_to='uploads/', default='profile.png')
    is_online = models.BooleanField(default=False)
    bio = models.TextField(max_length=250, blank=True, null=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, default=NONE)
    location = models.CharField(max_length=50, blank=True, null=True)

    REQUIRED_FIELDS = [
   	 'email',
    ]

    def __str__(self):
        return self.email