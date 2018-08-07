from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.response import Response

from . import serializers
from . import models


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ArticleSerializer
    queryset = models.Article.objects.none()

    def get_serializer_class(self):
        """
        Return nested serializer only if an author is inlined.
        """
        if self.action=='create' or self.action=='update':
            try:
                if isinstance(self.request.data['author'], int):
                    return serializers.RegArticleSerializer
            except:
                pass
        return serializers.ArticleSerializer

    def get_queryset(self):
        """
        Filter articles if a word is passed as a GET param
        For the filter the whole word needs to be matched
        TODO: Add more tests depending on the requirements (only 1 word has to be passed or process many words/phrases)
        """
        queryset = models.Article.objects.all()

        if self.request.GET.get('keyword'):
            keyword = self.request.GET.get('keyword')
            queryset = models.Article.objects.filter(body__iregex=r"\y{0}\y".format(keyword))
        return queryset

    #@cache_page(60 * 5)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()