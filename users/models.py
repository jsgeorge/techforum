from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

#User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', null=True, blank=True)
    bio = models.TextField(null=True,blank=True)
    overview = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def following_cnt(self):
            following = FollowUser.objects.filter(user=self)
            return len(following)

    def followed_cnt(self):
            followed = FollowUser.objects.filter(following=self)
            return len(followed)

    def __str__(self):
     return f'{self.user.username} Profile'

class UnivStudent(models.Model):
    """
    A class based model for storing the records of a university student
    Note: A OneToOne relation is established for each student with User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject_major = models.CharField(name="subject_major", max_length=60)

class FollowUser (models.Model):
    user = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="followee", on_delete=models.CASCADE)

    def __str__(self):
         return f'{self.user.username}'

