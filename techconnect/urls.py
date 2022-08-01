"""techconnect URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import *
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from posts.serializers import *
from rest_framework.urlpatterns import format_suffix_patterns

from posts.views import(
    PostViewSetREST,
    PostAPIView,
    LatestPostViewSetREST,
    RescentPostViewSetREST,
    # MostCommmentsPostViewSetREST,
    # MostLikesPostViewSetREST,
    CategoryViewSetREST,
    CommentViewSetREST,
    FavoriteViewSetREST,
    FollowCategoryViewSetREST,
   
)

from users.serializers import *
from users.views import(
    ProfileViewSetREST,
    UserViewSetREST,
    FollowUserViewSetREST,
    StudentRecordView,
    NotificationViewSetREST,
)

router = routers.DefaultRouter()
router.register('api/users', UserViewSetREST)
router.register('api/profile',ProfileViewSetREST)
router.register('api/following',FollowUserViewSetREST)
router.register('api/posts', PostViewSetREST)
router.register('api/posts/<int id>', PostViewSetREST)
router.register('api/favorites',FavoriteViewSetREST)
router.register("api/latest", LatestPostViewSetREST)
router.register("api/rescent", RescentPostViewSetREST)
# router.register("api/mostcomments",   MostCommmentsPostViewSetREST)
# router.register("api/mostlikes", MostLikesPostViewSetREST)
router.register('api/categories', CategoryViewSetREST)
router.register('api/followcategory', FollowCategoryViewSetREST)
router.register('api/comments', CommentViewSetREST)
router.register('api/notifications', NotificationViewSetREST)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', PostAPIView.as_view()),
    path('', include(router.urls)),
    path('api/auth/', obtain_auth_token) ,
    # path('api/univstud/',StudentRecordView.as_view(),name='students_list')
]
# urlpatterns += format_suffix_patterns([
#     # API to map the student record
#     path(r'^api/univstud/',
#         StudentRecordView.as_view(),
#         name='students_list'),
# ])
