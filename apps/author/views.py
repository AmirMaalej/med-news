from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from . import serializers
from . import models


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AuthorSerializer
    queryset = models.Author.objects.none()

    def get_serializer_class(self):
        return serializers.AuthorSerializer

    def get_queryset(self):
        return models.Author.objects.all()

    @method_decorator(never_cache)
    def list(self, request, *args, **kwargs):
        """
        list should not be cached
        """
        return super().list(request, *args, **kwargs)

    @method_decorator(never_cache)
    def retrieve(self, request, *args, **kwargs):
        """
        retrieve list should not be cached
        """
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()