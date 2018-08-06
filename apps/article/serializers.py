from rest_framework import serializers
from .mixins import NestedCreateMixin, NestedUpdateMixin

from apps.author.serializers import AuthorSerializer
from . import models


class ArticleSerializer(NestedCreateMixin, NestedUpdateMixin, serializers.ModelSerializer):
    """
    For inlined Author we use nested serializers
    """
    author = AuthorSerializer()

    class Meta:
        model = models.Article
        fields = ('id', 'title', 'body', 'author')


class RegArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Article
        fields = ('id', 'title', 'body', 'author')