from django.urls import path, include
from .views import *
from rest_framework.authtoken import views as auth_views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register('auth', AuthViewSet, basename="auth")
router.register(r'user-profiles', UserProfileViewSet)
router.register('articles', ArticleViewSet, basename='article')
router.register(r'comments', CommentViewSet)
router.register(r'likes', ArticleLikeViewSet)

urlpatterns = [
     path('', include(router.urls)),
     path('api-auth/', include('rest_framework.urls')),
     path('login/', auth_views.obtain_auth_token),
     ]