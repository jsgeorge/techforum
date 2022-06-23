from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
    
    # class Meta:
    #     model = Profile
    #     fields = ( 'id',  'user', 'image', 'bio', 'overview', 'created_at', 'following_cnt', 'followed_cnt',)
    
    def get_followers(self, obj):
        return obj.followers.count()

    def get_followed(self, obj):
        return obj.followed.count()


class UserSerializer(serializers.ModelSerializer):
    #profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        
        return user

class StudentSerializer(serializers.ModelSerializer):
    """
    A student serializer to return the student details
    """
    user = UserSerializer(required=True)

    class Meta:
        model = UnivStudent
        fields = ('user', 'subject_major',)

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        student, created = UnivStudent.objects.update_or_create(user=user,
                            subject_major=validated_data.pop('subject_major'))
        return student
        
class FollowUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUser
        fields = ['id', 'user', 'following']
