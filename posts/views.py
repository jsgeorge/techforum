import genericpath
from urllib import request
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework import serializers, viewsets, status, filters
from rest_framework.response import Response
# , api_view, authentication_classes, permission_classes
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.

class FollowCategoryViewSetREST(viewsets.ViewSet):
    serializer_class = FollowCategorySerializer
    queryset = FollowCategory.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)


    @action(detail=False, methods=['POST'])
    def userFavorite(self, request) :
        user = request.user
        print(request.data)
        if 'id' in request.data:
            id = request.data['id']
            print('userfavorite check')
            print ('ctgryid ', id)
            category = Category.objects.get(id=id)
            favorite = FollowCategory.objects.get(user=user, category=category)
            serializer = FollowCategorySerializer(favorite, many=False)
            response = {
                        'message': "Category unfollowed",
                        'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': "Error you need to provide category id"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



class CategoryViewSetREST(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['POST'])
    def follow(self, request, pk=None):
        print('follow', pk, request.data['follow'])
        #if 'like' in request.data:
        category = Category.objects.get(id=pk)
        user = request.user
        follow = request.data['follow']
        try:
            favorite = FollowCategory.objects.get(user=user, category=category)
            favorite.delete()
            serializer = FollowCategorySerializer(favorite, many=False)
            response = {
                    'message': "Category unfollowed",
                    'result': serializer.data}
            print("category unfolloweed")
            return Response(response, status=status.HTTP_200_OK)
        except:
            #save to favorites
            favorite = FollowCategory.objects.create(
                user=user,category=category)
            serializer = FollowCategorySerializer(favorite, many=False)
            response = {
                'message': "Category Followed",
                'result': serializer.data}
            print("category folloed")
            return Response(response, status=status.HTTP_200_OK)
    

class PostViewSetREST(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.order_by('created_at').reverse()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title','content']
    filterset_fields = ['category']

    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['GET'])
    def my_posts(self, request):
         user= request.user

         print(user)
         posts = Post.objects.filter(user=user).order_by('created_at').reverse()
         serializer =PostSerializer(posts,many=True)
         response = serializer.data
         return Response(response, status=status.HTTP_200_OK)
   
    @action(detail=False, methods=['POST'])
    def create_new(self, request):
         user = request.user
         print('user', user)
         title = request.data['title']
         category = Category.objects.get(id=request.data['category'])
         content = request.data['content']
         post= Post.objects.create(
             user = user,
             title=title,
             content=content,
             category=category
         )
         serializer=PostSerializer(post, many=False)
         response = {
                    'message': "Post created",
                    'result': serializer.data}
         return Response(response, status=status.HTTP_200_OK)
   
    @action(detail=True, methods=['POST'])
    def comment(self, request, pk=None):
        if 'content' in request.data:
            post = Post.objects.get(id=pk)
            user = request.user
            content = request.data['content']
        
            try:
                comment = Comment.objects.get(user=user, post=post)
                response = {'message': "Your already wrote a review for this Post"}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            except:
                comment = Comment.objects.create(
                    user=user,post=post, content=content)
                serializer = CommentSerializer(comment, many=False)
                response = {
                    'message': "Commentcreated",
                    'result': serializer.data}

                return Response(response, status=status.HTTP_200_OK)
                
        else:
            response = {'message': "Error you need to provide review"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def view_comments(self, request,pk=None):
                post = Post.objects.get(id=pk)
                list_item = Comment.objects.filter(post=post)
                serializer = CommentSerializer(list_item, many=True)
                response =  serializer.data
                print(response)
                return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        print('LIKE', request.data['like'])
        #if 'like' in request.data:
        post = Post.objects.get(id=pk)
        user = request.user
        like = request.data['like']
        try:
            favorite = Favorite.objects.get(user=user, post=post)
            favorite.delete()
            serializer = FavoriteSerializer(favorite, many=False)
            response = {
                    'message': "Favorite deleted",
                    'result': serializer.data}
            return Response(response, status=status.HTTP_200_OK)
        except:
            #save to favorites
            favorite = Favorite.objects.create(
                user=user,post=post)
            serializer = FavoriteSerializer(favorite, many=False)
            response = {
                'message': "Favorite created",
                'result': serializer.data}

            return Response(response, status=status.HTTP_200_OK)
    

class LatestPostViewSetREST(viewsets.ModelViewSet):
    
    #serializer_class = MovieMiniSerializer
    serializer_class = PostSerializer
    queryset = Post.objects.order_by('created_at').reverse()[:9]
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

class PostCtgryViewSetREST(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']

    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

  
class CommentViewSetREST(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
   
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

class FavoriteViewSetREST(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()[:6]
    serializer_class = FavoriteSerializer
   
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

      