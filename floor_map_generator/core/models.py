from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('user', 'User'),
        ('designer', 'Designer'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class FloorMap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    floor_type = models.CharField(max_length=20)
    width = models.FloatField()
    length = models.FloatField()
    num_rooms = models.IntegerField()
    num_bedrooms = models.IntegerField()
    num_kitchens = models.IntegerField()
    num_bathrooms = models.IntegerField()
    num_washrooms = models.IntegerField()
    description = models.TextField()
    prompt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('image', folder='floor_maps')

    def __str__(self):
        return self.name