import operator
from collections import OrderedDict
from functools import reduce

from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from itertools import chain

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
        The filter returns a list of articles ordered by those where the exact word is found in the body
        then the ones that contains the word in the body (substring)
        If you pass a whole phrase each word will be filtered separately
        TODO: maintain same result but minimize code ?
        """
        queryset = models.Article.objects.all()

        if self.request.GET.get('keyword'):
            keyword = self.request.GET.get('keyword')
            keyword_list = re.sub("[^\w]", " ", keyword).split()
            q = Q()
            qq = Q()
            for word in keyword_list:
                q |= Q(body__iregex=r"\y{0}\y".format(word))
                qq |= Q(body__icontains=word)
            queryset_iregex = queryset.filter(q)
            queryset_icontains = queryset.filter(qq)
            queryset = list(OrderedDict.fromkeys(chain(queryset_iregex, queryset_icontains)))

        return queryset

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        """
        Save the the result of list in cache for one hour
        """
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 60))
    def retrieve(self, request, *args, **kwargs):
        """
        Save the result of retrieve in cache for one hour
        """
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()