from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    image = models.ImageField(null=True, blank=True)
    desc = models.TextField(default="", null=True,blank=True)

    def post_cnt(self):
        posts = Post.objects.filter(category=self)
        return len(posts)

    def __str__(self):
        return self.name
    
    def imageURL(self):
            try:
                url = self.image.url
            except:
                url = ''
            return url


class FollowCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'category'),)
        index_together = (('user', 'category'),)

    def __str__(self):
        return self.category

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    category = models.ForeignKey(Category,null=True,
                                 on_delete=models.SET_NULL)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
   
    def comment_cnt(self):
        comments = Comment.objects.filter(post=self)
        return len(comments)

    def like_cnt(self):
        likes = Favorite.objects.filter(post=self)
        return len(likes)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post'),)
        index_together = (('user', 'post'),)

    def __str__(self):
        return self.post

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post'),)
        index_together = (('user', 'post'),)

    def __str__(self):
        return self.post

