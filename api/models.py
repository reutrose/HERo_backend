from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from taggit.managers import TaggableManager
from django.utils.text import slugify


STATUS_CHOICES = [
     ('draft', 'Draft'),
     ('published', 'Published'),
     ('archived', "Archived"),
]
LIKE_CHOICES = [
     ('like', 'Like'),
     ]

CATEGORY_CHOICES = [
     ("General", "General"),
     ("Technology", "Technology"),
     ("Wellness", "Wellness"),
     ("Health", "Health"),
     ("Fitness", "Fitness"),
     ("Nutrition", "Nutrition"),
     ("Beauty", "Beauty"),
     ("Fashion", "Fashion"),
     ("Lifestyle", "Lifestyle"),
     ("Motherhood", "Motherhood"),
     ("Parenting", "Parenting"),
     ("Relationships", "Relationships"),
     ("Selfcare", "Selfcare"),
     ("Mindset", "Mindset"),
     ("Career", "Career"),
     ("Finance", "Finance"),
     ("Business", "Business"),
     ("Leadership", "Leadership"),
     ("Empowerment", "Empowerment"),
     ("Education", "Education"),
     ("Travel", "Travel"),
     ("Home", "Home"),
     ("Entertainment", "Entertainment"),
     ("Community", "Community"),
]

class UserProfile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
     first_name = models.CharField(blank=True, max_length=150)
     last_name = models.CharField(blank=True, max_length=150)
     profession = models.CharField(blank=True, max_length=150)
     bio = models.TextField(blank=True, max_length=1000)
     profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
     birth_date = models.DateField(null=True, blank=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     @property
     def username(self):
          return self.user.username

     def __str__(self):
          return f'{self.user.username} Profile'

class Article(models.Model):
     author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='articles')
     title = models.CharField(
          max_length=100, 
          unique=True, 
          validators=[
               MinLengthValidator(5),
               MaxLengthValidator(100),
               RegexValidator(regex='^[a-zA-Z].*$', message="Title must start with a letter.")
          ]
     )
     slug = models.SlugField(unique=True, blank=True, null=True, max_length=255)
     category = models.CharField(
          max_length=100,
          choices=CATEGORY_CHOICES,
          default="General",
     )
     description = models.TextField(
          validators=[MinLengthValidator(10)],
          help_text="A short summary of the article.",
          blank=True,
          null=True
     )
     content = models.TextField(
          validators=[MinLengthValidator(10)],
          help_text="The content of the article.",
          blank=False,
          null=False
     )
     tags = TaggableManager()
     image = models.ImageField(upload_to="article_images/", blank=True, null=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='draft')

     def __str__(self):
          return f'{self.title} by {self.author.username}'
     
     def save(self, *args, **kwargs):
          if not self.slug:
               self.slug = slugify(self.title)
          super().save(*args, **kwargs)

class Comment(models.Model):
     author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
     article = models.ForeignKey(Article, on_delete=models.CASCADE)
     content = models.TextField(validators=[
          MinLengthValidator(2)
     ])
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     reply_to = models.ForeignKey(
          'self',
          on_delete=models.CASCADE,
          default=None,
          null=True,
          blank=True,
          related_name='replies',
     )

     def __str__(self):
          return f'{self.content} by {self.author.username}'

class ArticleLike(models.Model):
     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
     article = models.ForeignKey(Article, on_delete=models.CASCADE)
     reaction = models.CharField(choices=LIKE_CHOICES, max_length=10, default='like')
     created_at = models.DateTimeField(auto_now_add=True)

     class Meta:
          unique_together = ['user', 'article']

     def __str__(self):
          return f'{self.user.username} added a {self.reaction} to {self.article.title}'