from django.views.decorators.cache import cache_page
from rest_framework import viewsets

from . import serializers
from . import models


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.none()

    def get_serializer_class(self):
        if self.action=='create' or self.action=='update':
            try:
                if isinstance(self.request.data['author'], int):
                    return serializers.RegArticleSerializer
            except:
                pass
        return serializers.ArticleSerializer

    #@cache_page(60 * 5)
    def get_queryset(self):
        queryset = models.Article.objects.all()

        if self.request.GET.get('keyword'):
            keyword = self.request.GET.get('keyword')
            queryset = models.Article.objects.filter(body__iregex=r"\y{0}\y".format(keyword))
        return queryset

    def perform_create(self, serializer):
        serializer.save()