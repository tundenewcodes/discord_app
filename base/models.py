from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default='avatar.svg')
    USERNAME_FIELD: 'email'
    REQUIRED_FIELDS: []

#from django.contrib.auth.models import User
#Create your models here.
#a topic can have multiple rooms whereas a room can only have one topic
class Topic(models.Model):
    name = models.CharField(max_length=200)    
    def __str__(self):
        return self.name[:100]

class Room(models.Model):
    host  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    # to change the name that is shown in the database
    def __str__(self):
        return self.name
    # to change the order by which that is shown in the database  - is put there to make it a descending order
    class Meta:
        ordering = ['-updated', '-created']
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room  = models.ForeignKey(Room, on_delete=models.CASCADE) #for one to many relationship
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.body[:50]
    class Meta:
        ordering = ['-updated', '-created']

