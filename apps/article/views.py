from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets

import re

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
        Filter articles by a GET param if one was passed.
        The filter looks for the whole content as it is ('ill' doesn't return 'capillary')
        if it does not find any matches it will look for anything that contains the word
        If you pass a whole phrase each word will be filtered separately
        """
        queryset = models.Article.objects.all()

        if self.request.GET.get('keyword'):
            keyword = self.request.GET.get('keyword')
            keyword_list = re.sub("[^\w]", " ", keyword).split()
            q = Q()
            for word in keyword_list:
                q |= Q(body__iregex=r"\y{0}\y".format(word))
            queryset_iregex = queryset.filter(q)
            if queryset_iregex.count() < 1:
                for word in keyword_list:
                    q |= Q(body__icontains=word)
                queryset = queryset.filter(q)
            else:
                queryset = queryset_iregex
        return queryset

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        """
        Caching the result of list for one hour
        """
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60))
    def retrieve(self, request, *args, **kwargs):
        """
        Caching the result of retrieve for one hour
        """
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()