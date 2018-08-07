from django.db.models import Q
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.response import Response

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
            queryset1 = queryset.filter(q)
            if queryset1.count() < 1:
                for word in keyword_list:
                    q |= Q(body__icontains=word)
                queryset = queryset.filter(q)
            else:
                queryset = queryset1
        return queryset

    #@cache_page(60 * 5)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()