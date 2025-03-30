import re
from django.contrib.auth.models import User
from .models import UserProfile, Article, Comment, ArticleLike
from rest_framework.serializers import (
                                   ModelSerializer, 
                                   ValidationError, 
                                   SerializerMethodField, 
                                   HiddenField, 
                                   SerializerMethodField,
                                   CharField,
                                   PrimaryKeyRelatedField,
                                   UniqueTogetherValidator,
                                   )
from taggit.serializers import TagListSerializerField, TaggitSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.validations import validate_password_strength


class APITokenObtainPairSerializer(TokenObtainPairSerializer):
     @classmethod
     def get_token(cls, user):
          token = super().get_token(user)
          token['username'] = user.username
          token['role'] = "user"
          if user.groups.filter(name='Moderators').exists():
               token['role'] = "moderator"
          elif user.groups.filter(name='Admins').exists():
               token['role'] = 'admin'
          elif user.is_superuser:
               token['role'] = 'superuser'
          return token

class TagField(TagListSerializerField):
     def to_internal_value(self, value):
          request = self.context.get('request')
          is_browsable_api = (
               request
               and hasattr(request, 'accepted_renderer')
               and request.accepted_renderer.format == 'api'
          )
          if (
               is_browsable_api
               and isinstance(value, list)
               and isinstance(value[0], str)
               and len(value) == 1
          ):
               value = [tag.strip() for tag in re.split(r'[^a-zA-Z]+', value[0]) if tag.strip()]
          return super().to_internal_value(value)

class CurrentUserDefault():
     requires_context = True

     def __call__(self, serializer_field):
          request =  serializer_field.context['request']
          return request.user.userprofile

class UserSerializer(ModelSerializer):
     password = CharField(write_only=True, validators=[validate_password_strength])
     class Meta:
          model = User
          fields = ['id', 'username', 'password']
          extra_kwargs = {
               'password': {'write_only': False, 'required': True},
               'id': {'read_only': True, 'required': True},
               'username': {'required': True, 'min_length': 3},
          }

     def validate(self, attrs):
          if attrs['password'] == attrs['username']:
               raise ValidationError('Password must be different from username.')
          return super().validate(attrs)

     def create(self, validated_data):
          user = User.objects.create_user(**validated_data)
          return user

     def update(self, instance:User, validated_data):
          password = validated_data.pop('password', None)
          for key, value in validated_data.items():
               setattr(instance, key, value)
          if password:
               instance.set_password(password)
          instance.save()
          return instance

class UserProfileSerializer(ModelSerializer):
     class Meta:
          model = UserProfile
          fields = [
               'id', 'user_id', 'username', 'first_name', 'last_name', 'profession', 'bio', 'profile_pic', 
               'birth_date', 'created_at', 'updated_at'
          ]

class ArticleSerializer(TaggitSerializer, ModelSerializer):
     tags = TagField(style={'base_template': 'input.html'})
     author = HiddenField(default=CurrentUserDefault())
     author_id = SerializerMethodField()
     author_username = SerializerMethodField()
     likes = SerializerMethodField()

     class Meta:
          model = Article
          fields = [
               'id',
               'author',
               'author_id',
               'author_username',
               'title',
               'category',
               'description',
               'content',
               'tags',
               'image',
               'created_at',
               'updated_at',
               'likes',
               'status'
               ]

     def validate(self, attrs):
          request = self.context.get('request')
          if not request or not request.user or not request.user.is_authenticated:
               raise ValidationError("You must be logged in to create an article.")
          return attrs

     def get_author_id(self, obj):
          return obj.author.id

     def get_author_username(self, obj):
          return obj.author.user.username
     
     def get_likes(self, obj):
          return ArticleLike.objects.filter(article=obj).values_list("user_id", flat=True)

class CommentSerializer(ModelSerializer):
     author = HiddenField(default=CurrentUserDefault()) 
     author_id = SerializerMethodField() 
     author_username = SerializerMethodField()

     class Meta:
          model = Comment
          fields = '__all__'

     def validate(self, attrs):
          request = self.context.get('request')
          if not request or not request.user or not request.user.is_authenticated:
               raise ValidationError("You must be logged in to post a comment.")
          return attrs

     def get_author_id(self, obj):
          return obj.author.id

     def get_author_username(self, obj):
          return obj.author.user.username 

     def create(self, validated_data):
          reply_to = validated_data.get('reply_to')
          article = validated_data.get('article')
          if reply_to:  
               if reply_to.article != article:
                    raise ValidationError("Reply must be on the same article.")
               validated_data['reply_to'] = reply_to
          return super().create(validated_data)

class ArticleLikeSerializer(ModelSerializer):
     user = HiddenField(default=CurrentUserDefault())
     user_id = SerializerMethodField()
     user_username = SerializerMethodField()
     article = PrimaryKeyRelatedField(queryset=Article.objects.all())

     class Meta:
          model = ArticleLike
          validators = [
               UniqueTogetherValidator(
                    queryset=ArticleLike.objects.all(),
                    fields=('article', 'user'),
                    message="Each user is allowed to like an article only once."
               )
          ]
          fields = '__all__'

     def validate(self, attrs):
          request = self.context.get('request')
          if not request or not request.user or not request.user.is_authenticated:
               raise ValidationError("You must be logged in to like an article.")
          return attrs

     def get_user_id(self, obj):
          return obj.user.id

     def get_user_username(self, obj):
          return obj.user.username