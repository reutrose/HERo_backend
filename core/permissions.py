from api.models import *
from rest_framework.permissions import BasePermission, SAFE_METHODS

"""User Permissions"""
class UserPermissionClass(BasePermission):
     def has_permission(self, request, view):
          if request.method == 'GET':
               if request.user.is_authenticated:
                    return (
                         request.user == view.get_object() or
                         request.user.is_superuser or 
                         request.user.groups.filter(name='Admins').exists()
                         )
               return False
          
          elif request.method == 'PUT':
               return request.user == view.get_object()
          
          elif request.method == 'DELETE':
               if request.user.is_authenticated:
                    return (
                         request.user == view.get_object() or 
                         request.user.is_superuser or 
                         request.user.groups.filter(name='Admins').exists()
                         )
               return False
          
          return False
     
     def has_object_permission(self, request, view, obj):
          if request.method == 'GET':
               return (
                    obj == request.user or 
                    request.user.is_superuser or 
                    request.user.groups.filter(name='Admins').exists()
                    )
          elif request.method == 'POST':
               return (
                    request.user.is_superuser or 
                    request.user.groups.filter(name='Admins').exists()
                    )
          elif request.method == 'PUT':
               return obj == request.user
          elif request.method == 'DELETE':
               return (
                    obj == request.user or 
                    request.user.is_superuser or 
                    request.user.groups.filter(name='Admins').exists()
                    )
          return False

"""User Profile Permissions"""
class UserProfilePermissionClass(BasePermission):
     def has_permission(self, request, view):
          if request.method == 'GET':
               return True
          
          elif request.method == 'PUT':
               return request.user.id == view.get_object().user_id
          
          elif request.method == 'DELETE':
               return False
          
          return False
     
     def has_object_permission(self, request, view, obj):
          if request.method == 'GET':
               return True
          elif request.method == 'POST':
               return False
          elif request.method == 'PUT':
               return obj.user_id == request.user.id
          elif request.method == 'DELETE':
               return False
          return False

"""Articles Permissions"""
class GetArticles(BasePermission):
     def has_permission(self, request, view):
          return request.method in SAFE_METHODS

class CreateArticle(BasePermission):
     def has_permission(self, request, view):
          return request.user and request.user.is_authenticated and (
               request.user.groups.filter(name="Moderators").exists() or
               request.user.groups.filter(name="Admins").exists() or
               request.user.is_superuser
          )

class EditArticle(BasePermission):
     def has_object_permission(self, request, view, obj):
          if request.method in SAFE_METHODS:
               return True
          if request.method == 'PUT':
               return (
                    request.user and request.user.is_authenticated and (
                         obj.author_id == request.user.id and request.user.groups.filter(name="Moderators").exists() or
                         request.user.groups.filter(name="Admins").exists() or
                         request.user.is_superuser
                    )
               )
          return False

class DeleteArticle(BasePermission):
     def has_object_permission(self, request, view, obj):
          if request.method in SAFE_METHODS:
               return True
          if request.method == 'DELETE':
               return (
                    request.user and request.user.is_authenticated and (
                         obj.author_id == request.user.id and request.user.groups.filter(name="Moderators").exists() or
                         request.user.groups.filter(name="Admins").exists() or
                         request.user.is_superuser
                    )
               )
          return False

"""Comments Permissions"""
class GetComments(BasePermission):
     def has_permission(self, request, view):
          return request.method in SAFE_METHODS

class PostComment(BasePermission):
     def has_permission(self, request, view):
          return request.user and request.user.is_authenticated and (
               request.user.groups.filter(name="Users").exists() or
               request.user.groups.filter(name="Moderators").exists() or
               request.user.groups.filter(name="Admins").exists() or
               request.user.is_superuser
          )

class EditComment(BasePermission):
     def has_object_permission(self, request, view, obj):
          if request.method in SAFE_METHODS:
               return True
          if request.method in ['PUT', 'PATCH']:
               return (
                    request.user and request.user.is_authenticated and (
                         obj.author == request.user or
                         request.user.groups.filter(name="Moderators").exists() or
                         request.user.groups.filter(name="Admins").exists() or
                         request.user.is_superuser
                    )
               )
          return False

class DeleteComment(BasePermission):
     def has_object_permission(self, request, view, obj):
          if request.method in SAFE_METHODS:
               return True
          if request.method == 'DELETE':
               return (
                    request.user and request.user.is_authenticated and (
                         obj.author_id == request.user.id or
                         request.user.groups.filter(name="Admins").exists() or
                         request.user.is_superuser
                    )
               )
          return False

"""Article Likes Permissions"""
class GetArticleLikes(BasePermission):
     def has_permission(self, request, view):
          return request.method in SAFE_METHODS

class PostArticleLike(BasePermission):
     def has_permission(self, request, view):
          return request.user and request.user.is_authenticated and (
               request.user.groups.filter(name="Users").exists() or
               request.user.groups.filter(name="Moderators").exists() or
               request.user.groups.filter(name="Admins").exists() or
               request.user.is_superuser
          )

     def has_object_permission(self, request, view, obj):
          if request.method == 'POST':
               existing_like = ArticleLike.objects.filter(user=request.user, article=obj.article)
               return not existing_like.exists()
          return True

class DeleteArticleLike(BasePermission):
     def has_object_permission(self, request, view, obj):
          if request.method in SAFE_METHODS:
               return True
          if request.method == 'DELETE':
               return (
                    request.user and request.user.is_authenticated and (
                         obj.user_id == request.user.id
                    )
               )
          return False