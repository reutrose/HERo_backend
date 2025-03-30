from django_filters import rest_framework as filters
from .models import Article, Comment

class ArticleFilter(filters.FilterSet):
     tags = filters.CharFilter(method='filter_by_tags')
     category = filters.CharFilter(field_name='category', lookup_expr='iexact')

     class Meta:
          model = Article
          fields = ['title', 'author', 'created_at', 'updated_at', 'category']

     def filter_by_tags(self, queryset, name, value):
          return queryset.filter(tags__name__icontains=value)

class CommentFilter(filters.FilterSet):
     class Meta:
          model = Comment
          fields = ['author_id']