from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'desc', 'post_cnt']
   
    def get_posts(self, obj):
        return obj.posts.count()

class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    
    class Meta:
        model = Post
        fields = ['id',  'user', 'title', 'category',
                   'image', 'content',  'push_notifications', 'views',
                  'created_at', 'comment_cnt', 'like_cnt']
    
   
    def get_comments(self, obj):
        return obj.comments.count()

    def get_likes(self, obj):
        return obj.likes.count()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content','timestamp']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user',  'post']

class FollowCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowCategory
        fields = ['id', 'user',  'category']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'post', 'note']
