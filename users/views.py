import genericpath
from multiprocessing import allow_connection_pickling
import re
from urllib import request
from django.shortcuts import render
from .models import *
from .serializers import *
from  posts.models import *
from  posts.serializers import *
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework import serializers, viewsets, status, filters
from rest_framework.response import Response
# , api_view, authentication_classes, permission_classes
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from rest_framework.views import APIView

# Create your views here.

class UserViewSetREST(viewsets.ModelViewSet):
    UserModel = get_user_model()
    queryset = UserModel.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
    filter_backends = [SearchFilter]
    search_fields = ['last_name','first_name','username']
   
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['GET'])
    def current_user(self, request):
        serializer = UserSerializer(request.user, many=False)
        response = serializer.data
        #print(request.user.profile)
        return Response(response, status=status.HTTP_200_OK)
    
    # @api_view(['GET'])
    # def get_profile(request, *args, **kwargs):
    #     instance = Profile.objects.filter(user=request.user).first()
    #     print(instance)
    #     data = {}
    #     if instance:
    #         data =  ProfileSerializer(instance).data
    #     return Response(data, status=status.HTTP_200_OK)
    @action(detail=True, methods=['GET'])
    def get_profile(self, request, pk=None):
        user = User.objects.get(id=pk)
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, many=False)
        response = serializer.data
        #print(request.user.profile)
        return Response(response, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'])
    def following(self, request, pk=None):
        user = User.objects.get(id=pk)
        following = FollowUser.objects.filter(user=user)
        serializer = FollowUserSerializer(following, many=True)
        response = serializer.data
        #print(request.user.profile)
        return Response(response, status=status.HTTP_200_OK)
            
    @action(detail=True, methods=['GET'])
    def favorites(self, request, pk=None):
        user = User.objects.get(id=pk)
        following = FollowCategory.objects.filter(user=user)
        serializer = FollowCategorySerializer(following, many=True)
        response = serializer.data
        #print(request.user.profile)
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def follow(self, request, pk=None):
        print('follow', pk, request.data['follow'])
        #if 'like' in request.data:
        fuser = User.objects.get(id=pk)
        user = request.user
        follow = request.data['follow']
        try:
            favorite = FollowUser.objects.get(user=user, following=fuser)
            favorite.delete()
            serializer = FollowUserSerializer(favorite, many=False)
            response = {
                    'message': "User unfollowed",
                    'result': serializer.data}
            print("category unfolloweed")
            return Response(response, status=status.HTTP_200_OK)
        except:
            #save to favorites
            favorite = FollowUser.objects.create(
                user=user,following=fuser)
            serializer = FollowUserSerializer(favorite, many=False)
            response = {
                'message': "Category Followed",
                'result': serializer.data}
            print("category folloed")
            return Response(response, status=status.HTTP_200_OK)
    

class ProfileViewSetREST(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    # def get_queryset(self):
    #     if self.action == 'list':
    #         return self.queryset.filter(user=self.request.user)
    #     return self.queryset
    # def retrieve(self, request, username, *args, **kwargs):
    #     # Try to retrieve the requested profile and throw an exception if the
    #     # profile could not be found.
    #     try:
    #         # We use the `select_related` method to avoid making unnecessary
    #         # database calls.
    #         profile = Profile.objects.select_related('user').get(
    #             user__username=username
    #         )
    #     except Profile.DoesNotExist:
    #         raise

    #     serializer = self.serializer_class(profile)

    #     return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['GET'])
    def current(self, request):
        user_profile=Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(user_profile, many=False)
        response = serializer.data
        #print(request.user.profile)
        return Response(response, status=status.HTTP_200_OK)
    


class StudentRecordView(APIView):
    """
    A class based view for creating and fetching student records
    """
    def get(self, format=None):
        """
        Get all the student records
        :param format: Format of the student records to return to
        :return: Returns a list of student records
        """
        students = UnivStudent.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a student record
        :param format: Format of the student records to return to
        :param request: Request object for creating student
        :return: Returns a student record
        """
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)

class FollowUserViewSetREST(viewsets.ViewSet):
    serializer_class = FollowUserSerializer
    queryset = FollowUser.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
