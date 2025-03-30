from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.filters import OrderingFilter, SearchFilter
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import *
from core.authentication import get_tokens_for_user
from .models import *
from .serializers import *
from .filters import ArticleFilter, CommentFilter


class AuthViewSet(ViewSet):
     queryset = User.objects.all()
     serializer_class = UserSerializer
     permission_classes = [AllowAny]

     def list(self, request):
          return Response({
               "login": reverse('auth-login', request=request),
               "register": reverse('auth-register', request=request),
               "logout": reverse('auth-logout', request=request),
          })

     @action(detail=False, methods=['post','get'])
     def register(self, request):
          serializer = UserSerializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          user = serializer.save()

          token, _ = Token.objects.get_or_create(user=user)
          jwt = get_tokens_for_user(user)
          return Response({'token': token.key, 'jwt': jwt})

     @action(detail=False, methods=['post'])
     def login(self, request):
          serializer = AuthTokenSerializer(data=request.data, context={'request': request})
          serializer.is_valid(raise_exception=True)
          user = serializer.validated_data['user']
          token, _ = Token.objects.get_or_create(user=user)
          jwt = get_tokens_for_user(user)
          login(request, user)
          return Response({'token': token.key, 'jwt': jwt})

     @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
     def logout(self, request):
          try:
               logout(request)
               request.user.auth_token.delete()
          except:
               pass
          return Response({"message":"Logged out successfully!"})

@method_decorator(csrf_exempt, name='dispatch')
class UserViewSet(ModelViewSet):
     queryset = User.objects.all()
     serializer_class = UserSerializer
     permission_classes = [UserPermissionClass]

class UserProfileViewSet(ModelViewSet):
     queryset = UserProfile.objects.all()
     serializer_class = UserProfileSerializer
     permission_classes = [UserProfilePermissionClass]

@method_decorator(csrf_exempt, name='dispatch')
class ArticleViewSet(ModelViewSet):
     queryset = Article.objects.annotate(
          likes=Count("articlelike", filter=Q(articlelike__reaction="like"))
     ).order_by("-id")
     serializer_class = ArticleSerializer
     filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
     filterset_class = ArticleFilter
     search_fields = ["title"]

     def get_permissions(self):
          if self.action == "list" or self.action == "retrieve":
               permission_classes = [GetArticles]
          elif self.action == "create":
               permission_classes = [CreateArticle]
          elif self.action in ["update", "partial_update"]:
               permission_classes = [EditArticle]
          elif self.action == "destroy":
               permission_classes = [DeleteArticle]
          else:
               permission_classes = [GetArticles]
          return [permission() for permission in permission_classes]

     @action(detail=True, methods=['get'])
     def comments(self, request, pk=None):
          article = get_object_or_404(Article, pk=pk)
          comments = Comment.objects.filter(article=article).order_by('created_at')
          serializer = CommentSerializer(comments, many=True)
          return Response(serializer.data)

     @action(detail=True, methods=['get'])
     def likes(self, request, pk=None):
          article = get_object_or_404(Article, pk=pk)
          likes = ArticleLike.objects.filter(article=article).order_by('created_at')
          serializer = ArticleLikeSerializer(likes, many=True)
          return Response(serializer.data)

class ArticleLikeViewSet(ModelViewSet):
     queryset = ArticleLike.objects.all()
     serializer_class = ArticleLikeSerializer
     filter_backends = [OrderingFilter, DjangoFilterBackend]

     def get_permissions(self):
          if self.action == "list" or self.action == "retrieve":
               permission_classes = [GetArticleLikes]
          elif self.action == "create":
               permission_classes = [PostArticleLike]
          elif self.action == "destroy":
               permission_classes = [DeleteArticleLike]
          else:
               permission_classes = [GetArticleLikes] 
          return [permission() for permission in permission_classes]
     
class CommentViewSet(ModelViewSet):
     queryset = Comment.objects.all()
     serializer_class = CommentSerializer
     filter_backends = [OrderingFilter, DjangoFilterBackend]
     filterset_class = CommentFilter

     def get_permissions(self):
          if self.action == "list" or self.action == "retrieve":
               permission_classes = [GetComments]
          elif self.action == "create":
               permission_classes = [PostComment]
          elif self.action in ["update", "partial_update"]:
               permission_classes = [EditComment]
          elif self.action == "destroy":
               permission_classes = [DeleteComment]
          else:
               permission_classes = [GetComments]
          return [permission() for permission in permission_classes]

     def list(self, request, *args, **kwargs):
          res = super().list(request, *args, **kwargs)
          if not isinstance(res.data, list):
               return res
          comments = list(res.data)
          comments_dict = {comment["id"]: comment for comment in comments} 
          root_comments = []
          for comment in comments:
               parent_id = comment.get('reply_to')
               if parent_id is None:
                    root_comments.append(comment)
               else:
                    parent = comments_dict.get(parent_id)
                    if parent:
                         if "replies" not in parent:
                              parent["replies"] = []
                         parent["replies"].append(comment)
          res.data = root_comments
          return res